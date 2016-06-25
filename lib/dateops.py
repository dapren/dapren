"""
This module contains most commonly used date operations
"""

from datetime import datetime, timedelta
import inspect
import constants
from constants import logger
from constants import str_possible_values


def str2date(date_str, date_format):
    """
    This method takes a date string and its format and returns python datetime
     object
    :param date_str: Date string, example '2016-06-21'

    :param date_format: The format in which date_str is provided, for example
    '2015-06-13 05:05:06' is provided in format '%Y-%m-%d %H:%M:%S'

    List of date_format directives
    https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior

    :return: Python datetime object
    """
    return datetime.strptime(date_str, date_format)


def date2str(date, date_format):
    """
    This method takes a date and returns a string representing the date in the
    date_format

    :param date: Python datetime object

    :param date_format: Output format of the string representation of the date

    List of date_format directives
    https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior

    :return: String in the format specifed by date_format argument
    """
    return date.strftime(date_format)


def epoch2datetime(epoch):
    """
    This method return epoch time (that you get by executing Linux command
    'date +%s') to python datetime object

    :param epoch: Linux epoch time

    :return: Python datetime object
    """
    return datetime.fromtimestamp(epoch)


def localtime2utc(date):
    """
    This method converts local python datetime to utc python datetime

    :param date: Input python datetime object

    :return: Python datetime object in utc
    """
    return date + (datetime.utcnow() - datetime.now())


def utc2localtime(date):
    """
    This method converts utc python datetime to local python datetime

    :param date: Python datetime object in utc

    :return: Python datetime object in localtime
    """
    return date - (datetime.utcnow() - datetime.now())


def get_weekday_name(date, abbreviated_or_full):
    """
    This method return weekday for a python datetime object.

    :param date: Python datetime object

    :param abbreviated_or_full: When value of this param is 'abbreviated'
    then return locale specific weekday like 'Sun', if value is 'full' then
    return full locale specific weekday name like 'Sunday'

    :return: Returns abbreviated or full local specific locale name depending on
    value of param abbreviated_or_full
    """
    if abbreviated_or_full == constants.str_abbreviated:
        return date.strftime('%a')
    elif abbreviated_or_full == constants.str_full:
        return date.strftime('%A')
    else:
        err_msg = str_possible_values('abbreviated_or_full',
            [constants.str_abbreviated, constants.str_full])

        raise ValueError(err_msg)


def get_weekday_number(date):
    """
     Return weekday number as string. 0 is Sunday and 6 is Saturday.

    :param date: Python datetime object

    :return: Returns weekday number as string
    """
    return date.strftime('%w')


def get_day_of_month(date, padded_or_unpadded):
    """
    This method return the day of month as string. The result is padded or
    unpadded based on the value of 2nd argument

    :param date: Python datetime object

    :param padded_or_unpadded: When value of this param is 'padded'
    then return day of month like '01', if value is 'unpadded' then
    return day of month like '1'

    :return: Returns padded or unpadded day of month, as string, depending on
    value of argument padded_or_unpadded
    """
    if padded_or_unpadded == constants.str_padded:
        return date.strftime('%d')
    elif padded_or_unpadded == constants.str_unpadded:
        return str(int(date.strftime('%d')))
    else:
        err_msg = str_possible_values('padded_or_unpadded',
            [constants.str_padded, constants.str_unpadded])
        raise ValueError(err_msg)


def get_month_name(date, abbreviated_or_full):
    """
    This method return month for a python datetime object.

    :param date: Python datetime object

    :param abbreviated_or_full: When value of this param is 'abbreviated'
    then return locale specific month name like 'Jan', if value is 'full' then
    return full locale specific month name like 'January'

    :return: Returns abbreviated or full month name depending on
    value of param abbreviated_or_full
    """
    if abbreviated_or_full == constants.str_abbreviated:
        return date.strftime('%b')
    elif abbreviated_or_full == constants.str_full:
        return date.strftime('%B')
    else:
        err_msg = str_possible_values('abbreviated_or_full',
            [constants.str_abbreviated, constants.str_full])

        raise ValueError(err_msg)


def get_month_number(date, padded_or_unpadded):
    """
    This method return the month numberas string. The result is
    padded or unpadded based on the value of 2nd argument

    :param date: Python datetime object

    :param padded_or_unpadded: When value of this param is 'padded'
    then return padded month number like '01', if value is 'unpadded' then
    return unpadded month number like '1'

    :return: Returns padded or unpadded month number, as string, depending on
    value of argument padded_or_unpadded
    """
    if padded_or_unpadded == constants.str_padded:
        return date.strftime('%m')
    elif padded_or_unpadded == constants.str_unpadded:
        return str(int(date.strftime('%m')))
    else:
        err_msg = str_possible_values('padded_or_unpadded', [
            constants.str_padded, constants.str_unpadded])
        raise ValueError(err_msg)


def get_year(date):
    """
    Returns 4 digit year of the date
    """
    return date.strftime('%Y')


def get_hour(date, padded_or_unpadded):
    """
    This method return the hour as string. The result is
    padded or unpadded based on the value of 2nd argument

    :param date: Python datetime object

    :param padded_or_unpadded: When value of this param is 'padded'
    then return padded hour like '01', if value is 'unpadded' then
    return unpadded hour like '1'

    :return: Returns padded or unpadded hour, as string, depending on
    value of argument padded_or_unpadded
    """
    if padded_or_unpadded == constants.str_padded:
        return date.strftime('%H')
    elif padded_or_unpadded == constants.str_unpadded:
        return str(int(date.strftime('%H')))
    else:
        err_msg = str_possible_values('padded_or_unpadded', [
            constants.str_padded, constants.str_unpadded])
        raise ValueError(err_msg)


def get_minute(date, padded_or_unpadded):
    """
    This method return the minute as string. The result is
    padded or unpadded based on the value of 2nd argument

    :param date: Python datetime object

    :param padded_or_unpadded: When value of this param is 'padded'
    then return padded minute like '01', if value is 'unpadded' then
    return unpadded minute like '1'

    :return: Returns padded or unpadded minute, as string, depending on
    value of argument padded_or_unpadded
    """
    if padded_or_unpadded == constants.str_padded:
        return date.strftime('%M')
    elif padded_or_unpadded == constants.str_unpadded:
        return str(int(date.strftime('%M')))
    else:
        err_msg = str_possible_values('padded_or_unpadded', [
            constants.str_padded, constants.str_unpadded])
        raise ValueError(err_msg)


def get_second(date, padded_or_unpadded):
    """
    This method return the second as string. The result is
    padded or unpadded based on the value of 2nd argument

    :param date: Python datetime object

    :param padded_or_unpadded: When value of this param is 'padded'
    then return padded second like '01', if value is 'unpadded' then
    return unpadded second like '1'

    :return: Returns padded or unpadded second, as string, depending on
    value of argument padded_or_unpadded
    """
    if padded_or_unpadded == constants.str_padded:
        return date.strftime('%S')
    elif padded_or_unpadded == constants.str_unpadded:
        return str(int(date.strftime('%S')))
    else:
        err_msg = str_possible_values('padded_or_unpadded', [
            constants.str_padded, constants.str_unpadded])
        raise ValueError(err_msg)


def get_microsecond(date, padded_or_unpadded):
    """
    This method return the microsecond as string. The result is
    padded or unpadded based on the value of 2nd argument

    :param date: Python datetime object

    :param padded_or_unpadded: When value of this param is 'padded'
    then return padded microsecond like '01', if value is 'unpadded' then
    return unpadded microsecond like '1'

    :return: Returns padded or unpadded microsecond, as string, depending on
    value of argument padded_or_unpadded
    """
    if padded_or_unpadded == constants.str_padded:
        return date.strftime('%f')
    elif padded_or_unpadded == constants.str_unpadded:
        return str(int(date.strftime('%f')))
    else:
        err_msg = str_possible_values('padded_or_unpadded', [
            constants.str_padded, constants.str_unpadded])
        raise ValueError(err_msg)


def get_day_of_year(date, padded_or_unpadded):
    """
    This method return the day of year as string. The result is
    padded or unpadded based on the value of 2nd argument

    :param date: Python datetime object

    :param padded_or_unpadded: When value of this param is 'padded'
    then return padded day of year like '01', if value is 'unpadded' then
    return unpadded day of year like '1'

    :return: Returns padded or unpadded day of year, as string, depending on
    value of argument padded_or_unpadded
    """
    if padded_or_unpadded == constants.str_padded:
        return date.strftime('%j')
    elif padded_or_unpadded == constants.str_unpadded:
        return str(int(date.strftime('%j')))
    else:
        err_msg = str_possible_values('padded_or_unpadded', [
            constants.str_padded, constants.str_unpadded])
        raise ValueError(err_msg)


def get_week_of_year(date, padded_or_unpadded, start_Sunday_or_Monday):
    """
    This method return week of year as string. It returns the value padded or
    unpadded depending on value of 2nd argument. It start week from sunday
    or monday depending on value of 3rd argument

    :param date: Python datetime object

    :param padded_or_unpadded: When value of this param is 'padded'
    then return padded week of year like '01', if value is 'unpadded' then
    return unpadded week of year like '1'

    :param start_sunday_or_monday: Week can start from Sunday or Monday.
    Specify it here

    :return: It returns the value padded or
    unpadded depending on value of 2nd argument. It start week from sunday
    or monday depending on value of 3rd argument
    """
    if start_Sunday_or_Monday == constants.str_Sunday:
        week_of_year = date.strftime('%U')
    elif start_Sunday_or_Monday == constants.str_Monday:
        week_of_year = date.strftime('%W')
    else:
        err_msg = str_possible_values('start_Sunday_or_Monday', [
            constants.str_Sunday, constants.str_Monday])
        raise ValueError(err_msg)

    if padded_or_unpadded == constants.str_padded:
        return week_of_year
    elif padded_or_unpadded == constants.str_unpadded:
        return str(int(week_of_year))
    else:
        err_msg = str_possible_values('padded_or_unpadded', [
            constants.str_padded, constants.str_unpadded])
        raise ValueError(err_msg)


def today():
    """
    Returns Python datetime object with today's date
    """
    return datetime.today()


def yesterday():
    """
    Returns Python datetime object with yesterday's date
    """
    return datetime.today() - timedelta(1)


def seconds_elapsed(date1, date2):
    """
    Returns number of seconds elapsed between date1 and date2 (date1 - date2)
    """
    return (date1 - date2).total_seconds()


def add_seconds(date1, n_seconds):
    """
    Add n_seconds to Python datetime object date1 and return resultant date.
    To add 1 day then n_seconds will be 24*60*60
    """
    return date1 + timedelta(seconds=n_seconds)


def subtract_seconds(date1, n_seconds):
    """
    Subtract n_seconds to Python datetime object date1 and return resultant
    date.
    To subtract 1 day then n_seconds will be 24*60*60
    """
    return date1 - timedelta(seconds=n_seconds)


# -----------------------------------------------------------------------------
# ----------------------------------------------------------------- UNIT TESTS
# -----------------------------------------------------------------------------

def test_seconds_elapsed():
    logger.info("Testing " + inspect.stack()[0][3])

    date1 = str2date('2015-06-29', '%Y-%m-%d')
    date2 = str2date('2015-07-01', '%Y-%m-%d')

    input_diff = 2 * 24 * 60 * 60
    output_diff = seconds_elapsed(date2, date1)
    assert input_diff == output_diff


def test_subtract_seconds():
    logger.info("Testing " + inspect.stack()[0][3])

    input_date = str2date('2015-06-29', '%Y-%m-%d')
    output_date = subtract_seconds(input_date, 5*24*60*60)
    assert output_date == str2date('2015-06-24', '%Y-%m-%d')


def test_add_seconds():
    logger.info("Testing " + inspect.stack()[0][3])

    input_date = str2date('2015-06-29', '%Y-%m-%d')
    output_date = add_seconds(input_date, 5*24*60*60)
    assert output_date == str2date('2015-07-04', '%Y-%m-%d')


def test_str2date_date2str():
    logger.info("Testing " + inspect.stack()[0][3])

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
    logger.info("Testing " + inspect.stack()[0][3])

    actual = epoch2datetime(1424900481)
    expected = str2date('2015-02-25 13:41:21', '%Y-%m-%d %H:%M:%S')
    assert actual == expected


def test_utc2pst():
    logger.info("Testing " + inspect.stack()[0][3])

    utc_date = str2date('2015-03-01 09:00:00', '%Y-%m-%d %H:%M:%S')
    pst_date = utc2localtime(utc_date)
    pst_str = date2str(pst_date, '%Y-%m-%d %H:%M:%S')
    assert pst_str == '2015-03-01 01:00:00' or pst_str == '2015-03-01 02:00:00'


def test_pst2utc():
    logger.info("Testing " + inspect.stack()[0][3])

    pst_date = str2date('2015-03-01 09:00:00', '%Y-%m-%d %H:%M:%S')
    utc_date = localtime2utc(pst_date)
    utc_str = date2str(utc_date, '%Y-%m-%d %H:%M:%S')
    assert utc_str == '2015-03-01 16:59:59' or utc_str == '2015-03-01 15:59:59'


def test_get_weekday_name():
    logger.info("Testing " + inspect.stack()[0][3])

    date = str2date('2015-03-01 09:00:00', '%Y-%m-%d %H:%M:%S')
    expected = 'Sun'
    actual = get_weekday_name(date, constants.str_abbreviated)
    assert expected == actual


def test_get_weekday_number():
    logger.info("Testing " + inspect.stack()[0][3])

    date = str2date('2015-03-01 09:00:00', '%Y-%m-%d %H:%M:%S')
    expected = '0'
    actual = get_weekday_number(date)
    assert expected == actual


def test_get_day_of_month():
    logger.info("Testing " + inspect.stack()[0][3])

    date = str2date('2015-03-01 09:00:00', '%Y-%m-%d %H:%M:%S')
    expected = '01'
    actual = get_day_of_month(date, 'padded')
    assert expected == actual

    expected = '1'
    actual = get_day_of_month(date, 'unpadded')
    assert expected == actual


def test_get_weekday_name():
    logger.info("Testing " + inspect.stack()[0][3])

    date = str2date('2015-03-01 09:00:00', '%Y-%m-%d %H:%M:%S')
    expected = 'Sun'
    actual = get_weekday_name(date, constants.str_abbreviated)
    assert expected == actual


def test_get_weekday_number():
    logger.info("Testing " + inspect.stack()[0][3])

    date = str2date('2015-03-01 09:00:00', '%Y-%m-%d %H:%M:%S')
    expected = '0'
    actual = get_weekday_number(date)
    assert expected == actual


def test_get_month_name():
    logger.info("Testing " + inspect.stack()[0][3])

    date = str2date('2015-03-01 09:00:00', '%Y-%m-%d %H:%M:%S')
    expected = 'Mar'
    actual = get_month_name(date, constants.str_abbreviated)
    assert expected == actual

    expected = 'March'
    actual = get_month_name(date, constants.str_full)
    assert expected == actual


def test_get_month_number():
    logger.info("Testing " + inspect.stack()[0][3])

    date = str2date('2015-03-01 09:00:00', '%Y-%m-%d %H:%M:%S')
    expected = '03'
    actual = get_month_number(date, constants.str_padded)
    assert expected == actual

    expected = '3'
    actual = get_month_number(date, constants.str_unpadded)
    assert expected == actual


def test_get_year():
    logger.info("Testing " + inspect.stack()[0][3])

    date = str2date('2015-03-01 09:00:00', '%Y-%m-%d %H:%M:%S')
    expected = '2015'
    actual = get_year(date)
    assert expected == actual


def test_get_hour():
    logger.info("Testing " + inspect.stack()[0][3])

    date = str2date('2015-03-01 09:00:00', '%Y-%m-%d %H:%M:%S')
    expected = '09'
    actual = get_hour(date, constants.str_padded)
    assert expected == actual

    expected = '9'
    actual = get_hour(date, constants.str_unpadded)
    assert expected == actual


def test_get_minute():
    logger.info("Testing " + inspect.stack()[0][3])

    date = str2date('2015-03-01 09:09:07', '%Y-%m-%d %H:%M:%S')
    expected = '09'
    actual = get_minute(date, constants.str_padded)
    assert expected == actual

    expected = '9'
    actual = get_minute(date, constants.str_unpadded)
    assert expected == actual


def test_get_second():
    logger.info("Testing " + inspect.stack()[0][3])

    date = str2date('2015-03-01 09:09:07', '%Y-%m-%d %H:%M:%S')
    expected = '07'
    actual = get_second(date, constants.str_padded)
    assert expected == actual

    expected = '7'
    actual = get_second(date, constants.str_unpadded)
    assert expected == actual


def test_get_microsecond():
    logger.info("Testing " + inspect.stack()[0][3])

    date = str2date('2015-03-01 09:09:07.009777', '%Y-%m-%d %H:%M:%S.%f')
    expected = '009777'
    actual = get_microsecond(date, constants.str_padded)
    assert expected == actual

    expected = '9777'
    actual = get_microsecond(date, constants.str_unpadded)
    assert expected == actual


def test_get_day_of_year():
    logger.info("Testing " + inspect.stack()[0][3])

    date = str2date('2015-03-01 09:09:07.009777', '%Y-%m-%d %H:%M:%S.%f')
    expected = '060'
    actual = get_day_of_year(date, constants.str_padded)
    assert expected == actual

    expected = '60'
    actual = get_day_of_year(date, constants.str_unpadded)
    assert expected == actual


def test_get_week_of_year():
    logger.info("Testing " + inspect.stack()[0][3])

    date = str2date('2001-01-01 09:09:07.009777', '%Y-%m-%d %H:%M:%S.%f')
    expected = '0'
    actual = get_week_of_year(date, constants.str_unpadded,
                              constants.str_Sunday)
    assert expected == actual

    expected = '01'
    actual = get_week_of_year(date, constants.str_padded,constants.str_Monday)
    assert expected == actual


# -----------------------------------------------------------------------------
# ----------------------------------------------------------------------- MAIN
# -----------------------------------------------------------------------------
if __name__ == constants.str___main__:

    # Execute all test methods. All test methods should start with string
    # "test_"
    for name in dir():
        if name.startswith("test_"):
            eval(name)()

    logger.info("All tests run fine")
