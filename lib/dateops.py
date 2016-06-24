__author__ = 'dapren'

from datetime import datetime, timedelta
import inspect

import constants


def str2date(date_str, date_format):
    return datetime.strptime(date_str, date_format)


def date2str(date, date_format):
    return date.strftime(date_format)


def epoch2datetime(epoch):
    return datetime.fromtimestamp(epoch)


def pst2utc(date):
    return date + (datetime.utcnow() - datetime.now())


def utc2pst(date):
    return date - (datetime.utcnow() - datetime.now())


def get_weekday_name(date):
    return date.strftime('%a')


def get_week_of_year(date):
    return date.strftime('%U')


def today():
    return datetime.today().strftime('%Y-%m-%d')


def yesterday():
    return (datetime.today() - timedelta(1)).strftime('%Y-%m-%d')


def today_minus(n_days):
    return (datetime.today() - timedelta(n_days)).strftime('%Y-%m-%d')


def today_plus(n_days):
    return (datetime.today() + timedelta(n_days)).strftime('%Y-%m-%d')


def date_diff(date1, date2):
    return (date1 - date2).days


def date_minus(date1, n_days):
    return (date1 - timedelta(n_days)).strftime('%Y-%m-%d')


def date_plus(date1, n_days):
    return (date1 + timedelta(n_days)).strftime('%Y-%m-%d')



# -----------------------------------------------------------------------------
# ----------------------------------------------------------------- UNIT TESTS
# -----------------------------------------------------------------------------

def test_date_diff():
    logging.info("Testing " + inspect.stack()[0][3])

    date1 = str2date('2015-06-29', '%Y-%m-%d')
    date2 = str2date('2015-07-01', '%Y-%m-%d')

    input_diff = 2
    output_diff = date_diff(date1, date2)
    assert input_diff == output_diff


def test_date_minus():
    logging.info("Testing " + inspect.stack()[0][3])

    input_date = str2date('2015-06-29', '%Y-%m-%d')
    output_date = date_minus(input_date, 5)
    assert output_date == '2015-06-24'


def test_date_plus():
    logging.info("Testing " + inspect.stack()[0][3])

    input_date = str2date('2015-06-29', '%Y-%m-%d')
    output_date = date_plus(input_date, 5)
    assert output_date == '2015-07-04'


def test_str2date_date2str():
    logging.info("Testing " + inspect.stack()[0][3])

    input_date = '2015-06-13 05:05:06'
    converted_date = str2date(input_date, '%Y-%m-%d %H:%M:%S')
    output_date = date2str(converted_date, '%Y-%m-%d %H:%M:%S')
    assert input_date == output_date

    input_date = '2015-06-13'
    converted_date = str2date(input_date, '%Y-%m-%d')
    output_date = date2str(converted_date, '%Y-%m-%d')
    assert input_date == output_date

    input_date = '06/13/2015'
    converted_date = str2date(input_date, '%m/%d/%Y')
    output_date = date2str(converted_date, '%m/%d/%Y')
    assert input_date == output_date


def test_def_epoch2datetime():
    logging.info("Testing " + inspect.stack()[0][3])

    actual_date = epoch2datetime(1424900481)
    expected_date = str2date('2015-02-25 13:41:21', '%Y-%m-%d %H:%M:%S')
    assert actual_date == expected_date


def test_utc2pst():
    logging.info("Testing " + inspect.stack()[0][3])

    utc_date = str2date('2015-03-01 09:00:00', '%Y-%m-%d %H:%M:%S')
    pst_date = utc2pst(utc_date)

    pst_str = date2str(pst_date, '%Y-%m-%d %H:%M:%S')

    assert pst_str == '2015-03-01 01:00:00' or pst_str == '2015-03-01 02:00:00'


def test_pst2utc():
    logging.info("Testing " + inspect.stack()[0][3])

    pst_date = str2date('2015-03-01 09:00:00', '%Y-%m-%d %H:%M:%S')
    utc_date = pst2utc(pst_date)

    utc_str = date2str(utc_date, '%Y-%m-%d %H:%M:%S')

    assert utc_str == '2015-03-01 16:59:59' or utc_str == '2015-03-01 15:59:59'


def test_get_weekday_name():
    date = str2date('2015-03-01 09:00:00', '%Y-%m-%d %H:%M:%S')
    expected_weekday_name = 'Sun'
    actual_weekday_name = get_weekday_name(date)
    assert expected_weekday_name == actual_weekday_name

# -----------------------------------------------------------------------------
# ----------------------------------------------------------------------- MAIN
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(stream=sys.stdout,
                        level=constants.APPLICATION_LOG_LEVEL)

    test_str2date_date2str()
    test_def_epoch2datetime()
    test_utc2pst()
    test_pst2utc()
    test_get_weekday_name()
    test_date_diff()
    test_date_minus()
    test_date_plus()