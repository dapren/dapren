from __future__ import print_function
from __future__ import division
from lib.urlops import url2str
from lib.strops import extract_tags_from_html
from lib.strops import remove_html_tags
from lib.fileops import str2file
from lib.fileops import get_uniq_tmp_filename
from lib.constants import dapren_logger
from yahoo_finance import Share

def get_momemtum_tickers():
    """
    This function return the top 50 momemtum stock tickers scraped from site
    http://tradingstockalerts.com/PremiumAlerts/Momentum for the given day
    """
    table_list = []
    row_list = []
    col_list = []

    site = 'http://tradingstockalerts.com/PremiumAlerts/Momentum'

    # TODO: REmove this comment
    #html = url2str(site)
    html="nada"

    for table in extract_tags_from_html(html, 'table'):
        for tr in extract_tags_from_html(table, 'tr'):
            for td in extract_tags_from_html(tr, 'td'):
                col_list.append(td)

            row_list.append(col_list)
            col_list = []

        table_list.append(row_list)
        row_list = []

    input_table = []
    for table in table_list:
        if len(table) > 50:
            input_table = table

    momemtum_tickers = []
    for row in input_table:
        if len(row) > 5:
            momemtum_tickers.append(remove_html_tags(row[1]))

    # TODO: Remove this hardcoding
    momemtum_tickers = ['AXAS', 'TGA', 'PESI', 'PFIS', 'EFSC', 'TWMC', 'CF', 'SCWX', 'CUBE', 'GPS',
                        'MBUU', 'BWZ', 'NORD', 'ALEX', 'EBIX', 'ELP', 'FEYE', 'INSM', 'MINI', 'ZGNX', 'SNSS',
                        'GIB', 'RVNC', 'ACOR', 'CDXC', 'CFCOU', 'KFY', 'KSS', 'TFX', 'VIRC', 'ACIW', 'ANIK',
                        'AP', 'BUD', 'LSI', 'SIG', 'XIN', 'CNXR', 'DK', 'NLNK', 'KXI', 'APDN', 'ARCO', 'BRS',
                        'NOVN', 'SAP', 'ZEUS', 'ASIX', 'ATRI', 'BCC']

    if  len(momemtum_tickers) < 50:
        out_filename = get_uniq_tmp_filename()
        str2file(html, out_filename)
        msg="""Site {site} has either stopped returning top 50 momemtum stocks or the parsing logic is failing. To see the \
html returned from this site for this run, see file {out_filename}
        """.format(
            site=site,
            out_filename=out_filename
        )
        dapren_logger.error(msg)

        raise Exception(msg)

    return momemtum_tickers


def get_50d_200d_moving_average():
    # TODO: Uncomment this line
    #for momemtum_ticker in get_momemtum_tickers():
    for momemtum_ticker in ['FB','AXAS', 'TGA', 'PESI']:
        share = Share(momemtum_ticker)
        print (momemtum_ticker)
        print (share.get_price())
        print (share.get_50day_moving_avg())
        print (share.get_200day_moving_avg())

        print ("\n")

get_50d_200d_moving_average()
