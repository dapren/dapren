from __future__ import print_function
from __future__ import division
from lib.urlops import url2str
from lib.strops import extract_tags_from_html
from lib.strops import remove_html_tags
from lib.fileops import str2file
from lib.fileops import list2file
from lib.fileops import get_uniq_tmp_filename
from lib.constants import dapren_logger
from lib.constants import DAPREN_DB_DIR
from yahoo_finance import Share
import time
from lib.numops import unstringify_number
from lib.dateops import today
from lib.dateops import date2str

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
        html = url2str(site)

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
            revenue_one_yr_ago = unstringify_number(momemtum_stocks_revenue[momemtum_stock]['one_yr_ago'])
            revenue_two_yr_ago = unstringify_number(momemtum_stocks_revenue[momemtum_stock]['two_yr_ago'])
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
#                                                                                             MAIN
# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    ds = date2str(today(), '%Y-%m-%d')
    db_filename = DAPREN_DB_DIR + '/momemtum_stock.db'

    # todo: uncomment next 3 lines
    #momemtum_stocks = get_momemtum_stocks()
    #momemtum_stocks_daily_50d_200d_price = get_daily_50d_200d_price(momemtum_stocks)
    #momemtum_stocks_revenue = get_revenue(momemtum_stocks)

    # todo : delete next 3 lines
    momemtum_stocks = ['AXAS', 'TGA', 'PESI', 'PFIS', 'EFSC', 'TWMC', 'CF', 'SCWX', 'CUBE', 'GPS', 'MBUU', 'BWZ', 'NORD', 'ALEX', 'EBIX', 'ELP', 'FEYE', 'INSM', 'MINI', 'ZGNX', 'SNSS', 'GIB', 'RVNC', 'ACOR', 'CDXC', 'CFCOU', 'KFY', 'KSS', 'TFX', 'VIRC', 'ACIW', 'ANIK', 'AP', 'BUD', 'LSI', 'SIG', 'XIN', 'CNXR', 'DK', 'NLNK', 'KXI', 'APDN', 'ARCO', 'BRS', 'NOVN', 'SAP', 'ZEUS', 'ASIX', 'ATRI', 'BCC']
    momemtum_stocks_daily_50d_200d_price = {'SAP': {'price_50day_moving_avg': 105.47, 'price_today': 108.61, 'price_200day_moving_avg': 102.26}, 'ANIK': {'price_50day_moving_avg': 51.897, 'price_today': 55.475, 'price_200day_moving_avg': 47.376}, 'KSS': {'price_50day_moving_avg': 40.01, 'price_today': 42.05, 'price_200day_moving_avg': 39.16}, 'ACIW': {'price_50day_moving_avg': 22.44, 'price_today': 22.63, 'price_200day_moving_avg': 22.26}, 'ZEUS': {'price_50day_moving_avg': 17.62, 'price_today': 18.13, 'price_200day_moving_avg': 18.81}, 'INSM': {'price_50day_moving_avg': 15.12, 'price_today': 29.84, 'price_200day_moving_avg': 16.36}, 'BCC': {'price_50day_moving_avg': 29.7, 'price_today': 32.25, 'price_200day_moving_avg': 28.91}, 'SIG': {'price_50day_moving_avg': 59.517, 'price_today': 65.645, 'price_200day_moving_avg': 62.327}, 'EBIX': {'price_50day_moving_avg': 57.53, 'price_today': 56.65, 'price_200day_moving_avg': 58.25}, 'LSI': {'price_50day_moving_avg': 73.752, 'price_today': 82.615, 'price_200day_moving_avg': 77.909}, 'EFSC': {'price_50day_moving_avg': 38.83, 'price_today': 37.3, 'price_200day_moving_avg': 41.19}, 'ARCO': {'price_50day_moving_avg': 8.87, 'price_today': 9.15, 'price_200day_moving_avg': 8.11}, 'BWZ': {'price_50day_moving_avg': 32.1377, 'price_today': 32.6525, 'price_200day_moving_avg': 31.0178}, 'KFY': {'price_50day_moving_avg': 33.11, 'price_today': 35.47, 'price_200day_moving_avg': 32.54}, 'TGA': {'price_50day_moving_avg': 1.28, 'price_today': 1.25, 'price_200day_moving_avg': 1.43}, 'SNSS': {'price_50day_moving_avg': 2.351, 'price_today': 2.174, 'price_200day_moving_avg': 3.175}, 'SCWX': {'price_50day_moving_avg': 10.63, 'price_today': 11.09, 'price_200day_moving_avg': 10.16}, 'CFCOU': {'price_50day_moving_avg': 11.8643, 'price_today': 12.0704, 'price_200day_moving_avg': 11.4987}, 'ACOR': {'price_50day_moving_avg': 21.86, 'price_today': 22.7, 'price_200day_moving_avg': 20.3}, 'BUD': {'price_50day_moving_avg': 117.658, 'price_today': 121.308, 'price_200day_moving_avg': 114.047}, 'MINI': {'price_50day_moving_avg': 30.26, 'price_today': 32.4, 'price_200day_moving_avg': 29.75}, 'CUBE': {'price_50day_moving_avg': 24.48, 'price_today': 26.85, 'price_200day_moving_avg': 25.24}, 'NOVN': {'price_50day_moving_avg': 4.53, 'price_today': 5.65, 'price_200day_moving_avg': 5.02}, 'ATRI': {'price_50day_moving_avg': 630.26, 'price_today': 668.0, 'price_200day_moving_avg': 557.87}, 'ASIX': {'price_50day_moving_avg': 32.6011, 'price_today': 34.4416, 'price_200day_moving_avg': 29.6198}, 'CF': {'price_50day_moving_avg': 29.95, 'price_today': 32.2, 'price_200day_moving_avg': 28.87}, 'XIN': {'price_50day_moving_avg': 5.226, 'price_today': 5.225, 'price_200day_moving_avg': 4.88}, 'RVNC': {'price_50day_moving_avg': 23.46, 'price_today': 25.6, 'price_200day_moving_avg': 22.32}, 'AP': {'price_50day_moving_avg': 14.17, 'price_today': 16.25, 'price_200day_moving_avg': 14.65}, 'TWMC': {'price_50day_moving_avg': 1.74, 'price_today': 2.6, 'price_200day_moving_avg': 1.87}, 'FEYE': {'price_50day_moving_avg': 14.69, 'price_today': 16.0, 'price_200day_moving_avg': 13.84}, 'PFIS': {'price_50day_moving_avg': 41.59, 'price_today': 40.21, 'price_200day_moving_avg': 42.02}, 'ELP': {'price_50day_moving_avg': 8.781, 'price_today': 9.325, 'price_200day_moving_avg': 9.061}, 'VIRC': {'price_50day_moving_avg': 5.38, 'price_today': 5.7, 'price_200day_moving_avg': 4.66}, 'GPS': {'price_50day_moving_avg': 23.61, 'price_today': 25.72, 'price_200day_moving_avg': 23.71}, 'KXI': {'price_50day_moving_avg': 103.101, 'price_today': 103.6946, 'price_200day_moving_avg': 101.938}, 'ZGNX': {'price_50day_moving_avg': 12.36, 'price_today': 16.0, 'price_200day_moving_avg': 12.22}, 'ALEX': {'price_50day_moving_avg': 42.84, 'price_today': 45.07, 'price_200day_moving_avg': 43.01}, 'AXAS': {'price_50day_moving_avg': 1.692, 'price_today': 1.655, 'price_200day_moving_avg': 1.832}, 'PESI': {'price_50day_moving_avg': 3.58, 'price_today': 4.15, 'price_200day_moving_avg': 3.41}, 'BRS': {'price_50day_moving_avg': 7.84, 'price_today': 8.79, 'price_200day_moving_avg': 10.65}, 'CNXR': {'price_50day_moving_avg': 0.7218, 'price_today': 0.7399, 'price_200day_moving_avg': 0.9647}, 'TFX': {'price_50day_moving_avg': 211.09, 'price_today': 231.89, 'price_200day_moving_avg': 202.34}, 'NORD': {'price_50day_moving_avg': 32.74, 'price_today': 32.57, 'price_200day_moving_avg': 30.13}, 'DK': {'price_50day_moving_avg': 24.2294, 'price_today': 25.7201, 'price_200day_moving_avg': 24.6438}, 'CDXC': {'price_50day_moving_avg': 3.32, 'price_today': 4.03, 'price_200day_moving_avg': 3.15}, 'NLNK': {'price_50day_moving_avg': 7.21, 'price_today': 18.11, 'price_200day_moving_avg': 12.81}, 'APDN': {'price_50day_moving_avg': 1.87, 'price_today': 2.28, 'price_200day_moving_avg': 1.65}, 'GIB': {'price_50day_moving_avg': 51.05, 'price_today': 52.14, 'price_200day_moving_avg': 49.3}, 'MBUU': {'price_50day_moving_avg': 27.03, 'price_today': 26.42, 'price_200day_moving_avg': 24.34}}
    momemtum_stocks_revenue = {'SAP': {'two_yr_ago': '20.79B', 'three_yr_ago': '17.56B', 'one_yr_ago': '22.06B'}, 'ANIK': {'two_yr_ago': '93M', 'three_yr_ago': '105.59M', 'one_yr_ago': '103.38M'}, 'KSS': {'two_yr_ago': '19.2B', 'three_yr_ago': '19.02B', 'one_yr_ago': '18.69B'}, 'ACIW': {'two_yr_ago': '1.05B', 'three_yr_ago': '1.03B', 'one_yr_ago': '1.01B'}, 'ZEUS': {'two_yr_ago': '1.18B', 'three_yr_ago': '1.44B', 'one_yr_ago': '1.06B'}, 'INSM': {'two_yr_ago': '-', 'three_yr_ago': '-', 'one_yr_ago': '-'}, 'BCC': {'two_yr_ago': '3.63B', 'three_yr_ago': '3.57B', 'one_yr_ago': '3.91B'}, 'SIG': {'two_yr_ago': '6.55B', 'three_yr_ago': '5.74B', 'one_yr_ago': '6.41B'}, 'EBIX': {'two_yr_ago': '265.48M', 'three_yr_ago': '214.32M', 'one_yr_ago': '298.29M'}, 'LSI': {'two_yr_ago': '365.19M', 'three_yr_ago': '320.57M', 'one_yr_ago': '455.55M'}, 'CFCOU': {'two_yr_ago': '-', 'three_yr_ago': '-', 'one_yr_ago': '-'}, 'ARCO': {'two_yr_ago': '3.05B', 'three_yr_ago': '3.65B', 'one_yr_ago': '2.93B'}, 'KFY': {'two_yr_ago': '1.41B', 'three_yr_ago': '1.07B', 'one_yr_ago': '1.65B'}, 'TGA': {'two_yr_ago': '117.97M', 'three_yr_ago': '303.28M', 'one_yr_ago': '83.65M'}, 'SNSS': {'two_yr_ago': '3.06M', 'three_yr_ago': '5.73M', 'one_yr_ago': '2.54M'}, 'SCWX': {'two_yr_ago': '339.52M', 'three_yr_ago': '262.13M', 'one_yr_ago': '429.5M'}, 'ACOR': {'two_yr_ago': '492.66M', 'three_yr_ago': '401.48M', 'one_yr_ago': '519.6M'}, 'MINI': {'two_yr_ago': '530.78M', 'three_yr_ago': '445.47M', 'one_yr_ago': '508.62M'}, 'CUBE': {'two_yr_ago': '438.26M', 'three_yr_ago': '370.65M', 'one_yr_ago': '505.63M'}, 'ATRI': {'two_yr_ago': '145.73M', 'three_yr_ago': '140.76M', 'one_yr_ago': '143.49M'}, 'ASIX': {'two_yr_ago': '1.33B', 'three_yr_ago': '1.79B', 'one_yr_ago': '1.19B'}, 'RVNC': {'two_yr_ago': '300,000', 'three_yr_ago': '383,000', 'one_yr_ago': '300,000'}, 'XIN': {'two_yr_ago': '1.19B', 'three_yr_ago': '930.67M', 'one_yr_ago': '1.58B'}, 'CF': {'two_yr_ago': '4.31B', 'three_yr_ago': '4.74B', 'one_yr_ago': '3.69B'}, 'AP': {'two_yr_ago': '238.46M', 'three_yr_ago': '272.89M', 'one_yr_ago': '331.86M'}, 'TWMC': {'two_yr_ago': '339.5M', 'three_yr_ago': '358.49M', 'one_yr_ago': '353.47M'}, 'FEYE': {'two_yr_ago': '622.97M', 'three_yr_ago': '425.66M', 'one_yr_ago': '714.11M'}, 'ELP': {'two_yr_ago': '14.95B', 'three_yr_ago': '13.92B', 'one_yr_ago': '13.1B'}, 'VIRC': {'two_yr_ago': '168.6M', 'three_yr_ago': '164.05M', 'one_yr_ago': '173.42M'}, 'GPS': {'two_yr_ago': '15.8B', 'three_yr_ago': '16.44B', 'one_yr_ago': '15.52B'}, 'NOVN': {'two_yr_ago': '-', 'three_yr_ago': '112,000', 'one_yr_ago': '-'}, 'ZGNX': {'two_yr_ago': '27.18M', 'three_yr_ago': '40.53M', 'one_yr_ago': '28.85M'}, 'ALEX': {'two_yr_ago': '472.8M', 'three_yr_ago': '560M', 'one_yr_ago': '387.5M'}, 'AXAS': {'two_yr_ago': '67.03M', 'three_yr_ago': '133.78M', 'one_yr_ago': '56.56M'}, 'PESI': {'two_yr_ago': '62.38M', 'three_yr_ago': '57.07M', 'one_yr_ago': '51.22M'}, 'BRS': {'two_yr_ago': '1.72B', 'three_yr_ago': '1.86B', 'one_yr_ago': '1.4B'}, 'CNXR': {'two_yr_ago': '95.85M', 'three_yr_ago': '84.58M', 'one_yr_ago': '81.89M'}, 'TFX': {'two_yr_ago': '1.81B', 'three_yr_ago': '1.83B', 'one_yr_ago': '1.87B'}, 'NORD': {'two_yr_ago': '641.79M', 'three_yr_ago': '976.74M', 'one_yr_ago': '95.31M'}, 'DK': {'two_yr_ago': '4.78B', 'three_yr_ago': '8.32B', 'one_yr_ago': '4.2B'}, 'CDXC': {'two_yr_ago': '22.01M', 'three_yr_ago': '15.31M', 'one_yr_ago': '26.81M'}, 'NLNK': {'two_yr_ago': '68.5M', 'three_yr_ago': '172.59M', 'one_yr_ago': '35.77M'}, 'APDN': {'two_yr_ago': '9.01M', 'three_yr_ago': '2.72M', 'one_yr_ago': '4.19M'}, 'GIB': {'two_yr_ago': '10.29B', 'three_yr_ago': '10.5B', 'one_yr_ago': '10.68B'}, 'MBUU': {'two_yr_ago': '228.62M', 'three_yr_ago': '190.94M', 'one_yr_ago': '252.97M'}}

    momemtum_stocks_merged_data_file = merge_and_create_stock_data_file(
        ds,
        momemtum_stocks,
        momemtum_stocks_daily_50d_200d_price,
        momemtum_stocks_revenue
    )

    
    print (momemtum_stocks_merged_data_file)

