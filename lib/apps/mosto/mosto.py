from __future__ import print_function
from __future__ import division
import time

from lib.urlops import url2str
from lib.strops import extract_tags_from_html
from lib.strops import remove_html_tags
from lib.fileops import str2file
from lib.fileops import list2file
from lib.fileops import file2list
from lib.fileops import get_uniq_tmp_filename
from lib.constants import dapren_logger
from lib.constants import DAPREN_DB_DIR
from lib.constants import DAPREN_LIB_DIR
from lib.constants import char_comma
from yahoo_finance import Share
from lib.numops import unstringify_number
from lib.sqliteops import execute_script
from lib.sqliteops import load_data_from_file
from lib.sqliteops import execute
from lib.dateops import today
from lib.dateops import date2str

"""
Get list of momemtum Stocks
http://tradingstockalerts.com/PremiumAlerts/Momentum


Get 50d 200d moving average
https://github.com/lukaszbanasiak/yahoo-finance


Get annual revenue
http://www.marketwatch.com/investing/stock/PFIS/financials
https://finance.yahoo.com/quote/TTWO/financials?p=TTWO
"""

ds = date2str(today(), '%Y-%m-%d')
app_home_dir = DAPREN_LIB_DIR + '/apps/mosto'

query_what_to_buy = """
DELETE FROM fct_buy_daily WHERE ds = '{ds}';

INSERT INTO fct_buy_daily
SELECT
    ds,
    momemtum_stock,
    revenue_one_yr_ago,
    revenue_two_yr_ago,
    price_today,
    price_50day_moving_avg,
    price_200day_moving_avg,
    (1 - (revenue_two_yr_ago/revenue_one_yr_ago)) * 100 as percent_revenue_change
FROM
    fct_momemtum_stock_daily
WHERE
    ds = '{ds}'
    AND ((1 - (revenue_two_yr_ago/revenue_one_yr_ago)) * 100) > 18
    AND revenue_one_yr_ago > 1000000
    AND price_50day_moving_avg > price_200day_moving_avg
    AND price_today > price_50day_moving_avg;
""".format(ds=ds)


query_what_to_sell = """
DELETE FROM fct_sell_daily WHERE ds = '{ds}';

INSERT INTO fct_sell_daily
SELECT
    A.ds,
    A.momemtum_stock,
    A.revenue_one_yr_ago,
    A.revenue_two_yr_ago,
    A.price_today,
    A.price_50day_moving_avg,
    A.price_200day_moving_avg,
    B.purchase_price,
    B.ds_purchased,
    (A.price_today/B.purchase_price - 1) * 100 as percent_change_from_my_purchase_price,
    CASE
        WHEN A.price_50day_moving_avg < price_200day_moving_avg
            THEN 'price_50day_moving_avg < price_200day_moving_avg'
        WHEN ((A.price_today/B.purchase_price - 1) * 100) > 300
            THEN 'stock grew over 300%'
        WHEN ((A.price_today/B.purchase_price - 1) * 100) < -15
            THEN 'stock dropped more than 15%'
    END as reason_to_sell
FROM
    fct_momemtum_stock_daily A
INNER JOIN
    dim_momemtum_stocks_i_own B
    ON A.momemtum_stock = B.momemtum_stock
WHERE
    A.ds = '{ds}'
    AND (
        A.price_50day_moving_avg < A.price_200day_moving_avg
        OR ((A.price_today/B.purchase_price - 1) * 100) > 300
        OR ((A.price_today/B.purchase_price - 1) * 100) < -15
    );
""".format(ds=ds)


# -------------------------------------------------------------------------------------------------
#                                                                        Create DB tables
# -------------------------------------------------------------------------------------------------
def create_db_tables(db_filename):
    execute_script(
        db_filename=db_filename,
        query=" ".join(file2list(app_home_dir+'/mosto.sql'))
    )

    execute_script(
        db_filename=db_filename,
        query="DELETE FROM dim_momemtum_stocks_i_own"
    )

    num_lines_loaded = load_data_from_file(
            db_filename=db_filename,
            db_table_to_load='dim_momemtum_stocks_i_own',
            data_filename=app_home_dir+"/momemtum_stocks_i_own.txt",
            delimiter=char_comma
        )

# -------------------------------------------------------------------------------------------------
#                                                                          Get momemtum stock list
# -------------------------------------------------------------------------------------------------
def get_momemtum_stocks():
    """
    This function return the top 50 momemtum stock stocks scraped from site
    http://tradingstockalerts.com/PremiumAlerts/Momentum for the given day
    """
    table_list = []
    row_list = []
    col_list = []

    dapren_logger.info('Getting momemtum stocks from http://tradingstockalerts.com/PremiumAlerts/Momentum')
    site = 'http://tradingstockalerts.com/PremiumAlerts/Momentum'
    html = url2str(site)

    for table in extract_tags_from_html(html, 'table'):
        for tr in extract_tags_from_html(table, 'tr'):
            for td in extract_tags_from_html(tr, 'td'):
                col_list.append(td)

            row_list.append(col_list)
            col_list = []

        table_list.append(row_list)
        row_list = []

    # Take only table that we need
    input_table = []
    for table in table_list:
        if len(table) > 50:
            input_table = table

    momemtum_stocks = []
    for row in input_table:
        if len(row) > 5:
            momemtum_stocks.append(remove_html_tags(row[1]))

    if len(momemtum_stocks) < 50:
        out_filename = get_uniq_tmp_filename()
        str2file(html, out_filename)
        msg="""Site {site} has either stopped returning top 50 momemtum stocks or the parsing logic is failing. \
To see the html returned from this site for this run, see file {out_filename}
        """.format(
            site=site,
            out_filename=out_filename
        )
        dapren_logger.error(msg)

        raise Exception(msg)

    dapren_logger.info('momemtum_stocks:' + str(momemtum_stocks))
    return momemtum_stocks


# -------------------------------------------------------------------------------------------------
#                                                                        Get momemtum stock price
# -------------------------------------------------------------------------------------------------
def get_daily_50d_200d_price(momemtum_stocks):
    momemtum_stocks_daily_50d_200d_price = {}

    for momemtum_stock in momemtum_stocks:
        dapren_logger.info('Getting price for {momemtum_stock}'.format(momemtum_stock=momemtum_stock))

        share = Share(momemtum_stock)
        price_today = float(share.get_price())
        price_50day_moving_avg = float(share.get_50day_moving_avg())
        price_200day_moving_avg = float(share.get_200day_moving_avg())

        momemtum_stocks_daily_50d_200d_price[momemtum_stock] = {
            'price_today': price_today,
            'price_50day_moving_avg': price_50day_moving_avg,
            'price_200day_moving_avg': price_200day_moving_avg
        }

    dapren_logger.info('momemtum_stocks_daily_50d_200d_price=' + str(momemtum_stocks_daily_50d_200d_price))
    return momemtum_stocks_daily_50d_200d_price


# -------------------------------------------------------------------------------------------------
#                                                                        Get momemtum stock revenue
# -------------------------------------------------------------------------------------------------
def get_revenue(momemtum_stocks):
    momemtum_stocks_revenue = {}

    for stock in momemtum_stocks:
        time.sleep( 5 )
        dapren_logger.info('Getting revenue for {stock}'.format(stock=stock))

        table_list = []
        row_list = []
        col_list = []

        site = "http://www.marketwatch.com/investing/stock/{stock}/financials".format(stock=stock)
        try:
            html = url2str(site)
        except:
            dapren_logger.error("{site} cannot be reached".format(site=site))


        for table in extract_tags_from_html(html, 'table'):
            for tr in extract_tags_from_html(table, 'tr'):
                for td in extract_tags_from_html(tr, 'td'):
                    col_list.append(td)

                row_list.append(col_list)
                col_list = []

            table_list.append(row_list)
            row_list = []

        # Keep the table you need
        input_table = []
        for table in table_list:
            if str(table).find('Sales/Revenue') > -1:
                input_table = table
                break

        for row in input_table:
            if len(row) > 5 and str(row).find('Sales/Revenue') > -1:
                momemtum_stocks_revenue[stock] = {
                    'one_yr_ago': remove_html_tags(row[5]),
                    'two_yr_ago': remove_html_tags(row[4]),
                }

    dapren_logger.info('momemtum_stocks_revenue=' + str(momemtum_stocks_revenue))

    return momemtum_stocks_revenue


# -------------------------------------------------------------------------------------------------
#                                                                    Merge all momemtum stock data
# -------------------------------------------------------------------------------------------------
def merge_and_create_stock_data_file(
        ds,
        momemtum_stocks,
        momemtum_stocks_daily_50d_200d_price,
        momemtum_stocks_revenue,
):
    output_filename = get_uniq_tmp_filename()

    output_table = []
    # Merge all information together and prepare to load data into SQLLite
    for momemtum_stock in momemtum_stocks:

        if momemtum_stock not in momemtum_stocks_daily_50d_200d_price:
            dapren_logger.info('Ignoring momemtum_stock {momemtum_stock} since its not found in momemtum_stocks_daily_50d_200d_price'.format(momemtum_stock=momemtum_stock))
            output_list = [ds, momemtum_stock, 0, 0, 0, 0, 0]

        elif momemtum_stock not in momemtum_stocks_revenue:
            dapren_logger.info('Ignoring momemtum_stock {momemtum_stock} since its not found in momemtum_stocks_revenue'.format(momemtum_stock=momemtum_stock))
            output_list = [ds, momemtum_stock, 0, 0, 0, 0, 0]

        elif momemtum_stocks_revenue[momemtum_stock]['one_yr_ago'] == '-' or momemtum_stocks_revenue[momemtum_stock]['two_yr_ago'] == '-':
            dapren_logger.info('Ignoring momemtum_stock {momemtum_stock} since it does not have revenue for last 2 years'.format(momemtum_stock=momemtum_stock))
            output_list = [ds, momemtum_stock, 0, 0, 0, 0, 0]

        else:
            # If revenue is negative then make it 0
            revenue_one_yr_ago = momemtum_stocks_revenue[momemtum_stock]['one_yr_ago']
            if revenue_one_yr_ago.find('(') > -1:
                revenue_one_yr_ago = 0
            else:
                revenue_one_yr_ago = unstringify_number(revenue_one_yr_ago)

            revenue_two_yr_ago = momemtum_stocks_revenue[momemtum_stock]['two_yr_ago']
            if revenue_two_yr_ago.find('(') > -1:
                revenue_two_yr_ago = 0
            else:
                revenue_two_yr_ago = unstringify_number(revenue_two_yr_ago)

            price_today = momemtum_stocks_daily_50d_200d_price[momemtum_stock]['price_today']
            price_50day_moving_avg = momemtum_stocks_daily_50d_200d_price[momemtum_stock]['price_50day_moving_avg']
            price_200day_moving_avg = momemtum_stocks_daily_50d_200d_price[momemtum_stock]['price_200day_moving_avg']

            output_list = [
                ds,
                momemtum_stock,
                revenue_one_yr_ago,
                revenue_two_yr_ago,
                price_today,
                price_50day_moving_avg,
                price_200day_moving_avg,
            ]

        output_list = [ str(x) for x in output_list ]

        output_table.append("\t".join(output_list))

    list2file(
        list_to_output = output_table,
        file_name = output_filename,
        mode = 'w'
    )
    return output_filename


# -------------------------------------------------------------------------------------------------
#                                                                    Load fct_momemtum_stock_daily
# -------------------------------------------------------------------------------------------------
def populate_fct_momemtum_stock_daily(db_filename, momemtum_stocks_merged_data_file):

    query = "DELETE FROM fct_momemtum_stock_daily WHERE ds = '{ds}'".format(ds=ds)
    execute_script(
        db_filename=db_filename,
        query=query
    )

    num_lines_loaded = load_data_from_file(
        db_filename=db_filename,
        db_table_to_load='fct_momemtum_stock_daily',
        data_filename=momemtum_stocks_merged_data_file,
    )

    dapren_logger.info("Loaded {num_lines_loaded} rows to table fct_momemtum_stock_daily".format(
        num_lines_loaded=num_lines_loaded)
    )

    return num_lines_loaded


# -------------------------------------------------------------------------------------------------
#                                                             Load fct_buy_daily & fct_sell_daily
# -------------------------------------------------------------------------------------------------
def populate_buy_sell_tables(db_filename):
    execute_script(
        db_filename=db_filename,
        query=query_what_to_buy
    )

    execute_script(
        db_filename=db_filename,
        query=query_what_to_sell
    )


# -------------------------------------------------------------------------------------------------
#                                                             Display what to buy and sell
# -------------------------------------------------------------------------------------------------
def display_what_to_buy_and_sell(db_filename):
    time.sleep(2)
    for type in ['buy', 'sell']:
        print("\n----- {type} ------".format(type=type.upper()))
        for row in execute(db_filename=db_filename,query="select * from fct_{type}_daily where ds = '{ds}'".format(
                ds=ds,
                type=type)):
            for col in row:
                print(str(col).ljust(25,' '), end="|")
            print ("")



# -------------------------------------------------------------------------------------------------
#                                                                                             MAIN
# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # Create required table structures and load default data
    db_filename = DAPREN_DB_DIR + '/momemtum_stock.db'
    create_db_tables(db_filename)

    # Manually monitor some stocks for momemtum
    other_momemtum_stock_list = file2list(app_home_dir+'/other_momemtum_stocks_to_watch.txt')

    # Get data from Web and process it
    momemtum_stocks = get_momemtum_stocks()
    momemtum_stocks = set(momemtum_stocks + other_momemtum_stock_list)
    momemtum_stocks_daily_50d_200d_price = get_daily_50d_200d_price(momemtum_stocks)
    momemtum_stocks_revenue = get_revenue(momemtum_stocks)

    # todo : delete next 3 lines
    #momemtum_stocks=['AROW', 'ISBC', 'TIVO', 'EBTC', 'XBKS', 'MDCA', 'WILC', 'LANDP', 'HBANN', 'HDS', 'MARA', 'RESN', 'ANGI', 'PNBK', 'HSGX', 'AGNC', 'GOVNI', 'WLTW', 'CBK', 'DOW', 'LQ', 'ZUMZ', 'AJG', 'PEB', 'SGB', 'XTN', 'SFE', 'AGX', 'DVD', 'HE', 'INBK', 'JXSB', 'DRIP', 'GIFI', 'MFCB', 'OLLI', 'CALA', 'CVRR', 'BV', 'COO', 'MSON', 'OCX', 'SCID', 'WDFC', 'CRIS', 'FOMX', 'FORK', 'FXE', 'FXSG', 'IBND']
    #momemtum_stocks = set(momemtum_stocks + other_momemtum_stock_list)
    #momemtum_stocks_daily_50d_200d_price={'OLLI': {'price_50day_moving_avg': 44.03, 'price_today': 45.2, 'price_200day_moving_avg': 39.26}, 'CVRR': {'price_50day_moving_avg': 7.83, 'price_today': 8.8, 'price_200day_moving_avg': 9.29}, 'HDS': {'price_50day_moving_avg': 31.76, 'price_today': 33.45, 'price_200day_moving_avg': 36.48}, 'WDFC': {'price_50day_moving_avg': 106.58, 'price_today': 108.1, 'price_200day_moving_avg': 107.43}, 'ISBC': {'price_50day_moving_avg': 13.11, 'price_today': 12.87, 'price_200day_moving_avg': 13.66}, 'ZUMZ': {'price_50day_moving_avg': 12.66, 'price_today': 16.3, 'price_200day_moving_avg': 15.11}, 'IBND': {'price_50day_moving_avg': 34.68, 'price_today': 35.36, 'price_200day_moving_avg': 32.76}, 'TIVO': {'price_50day_moving_avg': 18.53, 'price_today': 18.1, 'price_200day_moving_avg': 18.41}, 'OCX': {'price_50day_moving_avg': 4.81, 'price_today': 5.55, 'price_200day_moving_avg': 5.38}, 'BV': {'price_50day_moving_avg': 4.67, 'price_today': 4.95, 'price_200day_moving_avg': 4.58}, 'AGX': {'price_50day_moving_avg': 62.75, 'price_today': 62.55, 'price_200day_moving_avg': 64.59}, 'DOW': {'price_50day_moving_avg': 64.79, 'price_today': 66.65, 'price_200day_moving_avg': 63.46}, 'GOVNI': {'price_50day_moving_avg': 25.88, 'price_today': 25.73, 'price_200day_moving_avg': 25.43}, 'HE': {'price_50day_moving_avg': 33.19, 'price_today': 34.13, 'price_200day_moving_avg': 33.11}, 'MFCB': {'price_50day_moving_avg': 8.71, 'price_today': 9.2, 'price_200day_moving_avg': 8.61}, 'AROW': {'price_50day_moving_avg': 32.19, 'price_today': 31.8, 'price_200day_moving_avg': 33.02}, 'XBKS': {'price_50day_moving_avg': 28.73, 'price_today': 28.52, 'price_200day_moving_avg': 28.21}, 'DRIP': {'price_50day_moving_avg': 24.59, 'price_today': 25.89, 'price_200day_moving_avg': 20.99}, 'HSGX': {'price_50day_moving_avg': 1.83, 'price_today': 1.92, 'price_200day_moving_avg': 1.75}, 'MSON': {'price_50day_moving_avg': 9.18, 'price_today': 10.15, 'price_200day_moving_avg': 10.06}, 'PEB': {'price_50day_moving_avg': 32.66, 'price_today': 34.29, 'price_200day_moving_avg': 31.11}, 'LQ': {'price_50day_moving_avg': 15.31, 'price_today': 16.03, 'price_200day_moving_avg': 14.35}, 'GIFI': {'price_50day_moving_avg': 11.18, 'price_today': 11.65, 'price_200day_moving_avg': 10.7}, 'MDCA': {'price_50day_moving_avg': 10.06, 'price_today': 9.45, 'price_200day_moving_avg': 9.18}, 'WLTW': {'price_50day_moving_avg': 148.85, 'price_today': 151.84, 'price_200day_moving_avg': 140.4}, 'FORK': {'price_50day_moving_avg': 3.3, 'price_today': 3.6, 'price_200day_moving_avg': 3.23}, 'AGNC': {'price_50day_moving_avg': 21.31, 'price_today': 21.36, 'price_200day_moving_avg': 20.72}, 'JXSB': {'price_50day_moving_avg': 30.13, 'price_today': 30.39, 'price_200day_moving_avg': 30.33}, 'FOMX': {'price_50day_moving_avg': 4.9, 'price_today': 5.69, 'price_200day_moving_avg': 5.57}, 'RESN': {'price_50day_moving_avg': 4.59, 'price_today': 5.03, 'price_200day_moving_avg': 4.65}, 'CRIS': {'price_50day_moving_avg': 1.84, 'price_today': 2.16, 'price_200day_moving_avg': 2.15}, 'FXE': {'price_50day_moving_avg': 114.19, 'price_today': 116.17, 'price_200day_moving_avg': 108.26}, 'XTN': {'price_50day_moving_avg': 55.42, 'price_today': 57.65, 'price_200day_moving_avg': 54.24}, 'EBTC': {'price_50day_moving_avg': 32.69, 'price_today': 32.54, 'price_200day_moving_avg': 33.28}, 'AJG': {'price_50day_moving_avg': 58.52, 'price_today': 59.69, 'price_200day_moving_avg': 57.14}, 'LANDP': {'price_50day_moving_avg': 26.0597, 'price_today': 25.8384, 'price_200day_moving_avg': 25.9281}, 'HBANN': {'price_50day_moving_avg': 26.0, 'price_today': 25.8, 'price_200day_moving_avg': 25.44}, 'SGB': {'price_50day_moving_avg': 19.64, 'price_today': 21.99, 'price_200day_moving_avg': 20.68}, 'FXSG': {'price_50day_moving_avg': 72.4637, 'price_today': 73.3884, 'price_200day_moving_avg': 70.8063}, 'MARA': {'price_50day_moving_avg': 0.305, 'price_today': 0.435, 'price_200day_moving_avg': 0.552}, 'CBK': {'price_50day_moving_avg': 1.38, 'price_today': 1.46, 'price_200day_moving_avg': 1.31}, 'PNBK': {'price_50day_moving_avg': 16.74, 'price_today': 17.35, 'price_200day_moving_avg': 15.83}, 'ANGI': {'price_50day_moving_avg': 12.04, 'price_today': 12.13, 'price_200day_moving_avg': 9.79}, 'COO': {'price_50day_moving_avg': 245.26, 'price_today': 251.48, 'price_200day_moving_avg': 222.76}, 'SCID': {'price_50day_moving_avg': 27.4429, 'price_today': 27.8266, 'price_200day_moving_avg': 25.8701}, 'INBK': {'price_50day_moving_avg': 31.11, 'price_today': 30.5, 'price_200day_moving_avg': 29.24}, 'CALA': {'price_50day_moving_avg': 15.1, 'price_today': 16.25, 'price_200day_moving_avg': 13.78}, 'SFE': {'price_50day_moving_avg': 12.01, 'price_today': 12.6, 'price_200day_moving_avg': 12.03}, 'DVD': {'price_50day_moving_avg': 2.06, 'price_today': 2.3, 'price_200day_moving_avg': 2.1}, 'WILC': {'price_50day_moving_avg': 6.53, 'price_today': 6.0, 'price_200day_moving_avg': 6.55}}
    #momemtum_stocks_revenue={'OLLI': {'two_yr_ago': '762.37M', 'one_yr_ago': '890.32M'}, 'CVRR': {'two_yr_ago': '5.16B', 'one_yr_ago': '4.43B'}, 'HDS': {'two_yr_ago': '7.12B', 'one_yr_ago': '7.44B'}, 'WDFC': {'two_yr_ago': '378.15M', 'one_yr_ago': '380.67M'}, 'DVD': {'two_yr_ago': '46.54M', 'one_yr_ago': '45.87M'}, 'ZUMZ': {'two_yr_ago': '804.18M', 'one_yr_ago': '836.27M'}, 'TIVO': {'two_yr_ago': '542.31M', 'one_yr_ago': '526.27M'}, 'OCX': {'two_yr_ago': '-', 'one_yr_ago': '-'}, 'BV': {'two_yr_ago': '199.77M', 'one_yr_ago': '204.58M'}, 'AGX': {'two_yr_ago': '413.28M', 'one_yr_ago': '675.05M'}, 'DOW': {'two_yr_ago': '6.85B', 'one_yr_ago': '7.27B'}, 'PEB': {'two_yr_ago': '776.26M', 'one_yr_ago': '822.62M'}, 'HE': {'two_yr_ago': '2.6B', 'one_yr_ago': '2.38B'}, 'MFCB': {'two_yr_ago': '1.27B', 'one_yr_ago': '854.04M'}, 'HSGX': {'two_yr_ago': '-', 'one_yr_ago': '-'}, 'MSON': {'two_yr_ago': '23.11M', 'one_yr_ago': '27.27M'}, 'GOVNI': {'two_yr_ago': '249.7M', 'one_yr_ago': '259.64M'}, 'LQ': {'two_yr_ago': '1.03B', 'one_yr_ago': '1.01B'}, 'MDCA': {'two_yr_ago': '1.33B', 'one_yr_ago': '1.39B'}, 'WLTW': {'two_yr_ago': '3.83B', 'one_yr_ago': '7.85B'}, 'FORK': {'two_yr_ago': '91.29M', 'one_yr_ago': '104.88M'}, 'AGNC': {'two_yr_ago': '922M', 'one_yr_ago': '(11M)'}, 'FOMX': {'two_yr_ago': '849,000', 'one_yr_ago': '5.53M'}, 'RESN': {'two_yr_ago': '-', 'one_yr_ago': '302,000'}, 'CRIS': {'two_yr_ago': '7.88M', 'one_yr_ago': '7.53M'}, 'AJG': {'two_yr_ago': '5.39B', 'one_yr_ago': '5.59B'}, 'LANDP': {'two_yr_ago': '11.74M', 'one_yr_ago': '17.28M'}, 'GIFI': {'two_yr_ago': '306.12M', 'one_yr_ago': '286.33M'}, 'MARA': {'two_yr_ago': '18.98M', 'one_yr_ago': '36.63M'}, 'CBK': {'two_yr_ago': '383.83M', 'one_yr_ago': '381.61M'}, 'ANGI': {'two_yr_ago': '344.13M', 'one_yr_ago': '323.33M'}, 'COO': {'two_yr_ago': '1.8B', 'one_yr_ago': '1.97B'}, 'CALA': {'two_yr_ago': '-', 'one_yr_ago': '-'}, 'SFE': {'two_yr_ago': '-', 'one_yr_ago': '-'}, 'WILC': {'two_yr_ago': '80.44M', 'one_yr_ago': '76.64M'}}

    momemtum_stocks_merged_data_file = merge_and_create_stock_data_file(
        ds,
        momemtum_stocks,
        momemtum_stocks_daily_50d_200d_price,
        momemtum_stocks_revenue
    )

    # Load momemtum_stock price and revenue data into db
    populate_fct_momemtum_stock_daily(db_filename, momemtum_stocks_merged_data_file)

    # Find what to buy and sell
    populate_buy_sell_tables(db_filename)
    display_what_to_buy_and_sell(db_filename)
