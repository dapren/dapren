from __future__ import print_function
import constants
import inspect
from constants import logger

def stringify_number(number, **args_map):
    """
    Appends "K" in thousands, "M" in Million, "B" in Billions
    By default decimals are ignored
    :param number:
    :return: Number appended with "K" in thousands, "M" in Million,
             "B" in Billions
    """

    # Process argument map of the method
    __ignore_decimal = args_map.get('ignore_decimal', True)

    suffix = ""
    prefix = ""

    if str(number).startswith('-'):
        number = str(number).replace('-', '')
        prefix = '-'

    str_number = format(float(number), '.2f').split(".")

    if len(str_number[0]) >= 13:
        output_number = float(number) / 1000000000000
        suffix = "T"

    elif len(str_number[0]) >= 10:
        output_number = float(number) / 1000000000
        suffix = "B"

    elif len(str_number[0]) >= 7:
        output_number = float(number) / 1000000
        suffix = "M"

    elif len(str_number[0]) >= 4:
        output_number = float(number) / 1000
        suffix = "K"

    else:
        output_number = float(number)

    if __ignore_decimal is True:
        output_number = int(output_number)
    else:
        output_number = ("{0:.2f}".format(output_number)).replace(".00", "")

    return prefix + str(output_number) + suffix


def commafy_number(number, **args_map):
    """
    Add comma's in number. By default decimals are *not* ignored
    :param number:
    :param args_map:
    :return: Number with comma's inserted in number
    """

    # Process argument map of the method
    __ignore_decimal = args_map.get('ignore_decimal', False)

    # Implement method logic
    prefix = ""

    if str(number).startswith('-'):
        number = str(number).replace('-', '')
        prefix = '-'

    str_number = format(float(number), '.2f').replace('.00', '').split(".")

    r = []
    for i, c in enumerate(reversed(str_number[0])):
        if i and (not (i % 3)):
            r.insert(0, ',')
        r.insert(0, c)

    if len(str_number) == 2 and __ignore_decimal is False:
        return prefix + (''.join(r)) + "." + str_number[1]

    return prefix + ''.join(r)


# -----------------------------------------------------------------------------
# ----------------------------------------------------------------- UNIT TESTS
# -----------------------------------------------------------------------------
def test_stringify_number():
    logger.info("Testing " + inspect.stack()[0][3])

    assert stringify_number(123445678439, ignore_decimal=False) == '123.45B'
    assert stringify_number(0) == '0'
    assert stringify_number(51211237) == '51M'
    assert stringify_number(51211237, ignore_decimal=False) == '51.21M'
    assert stringify_number(512) == '512'
    assert stringify_number(547856789.234) == '547M'
    assert stringify_number(49078564378899.234) == '49T'
    assert stringify_number(40078564378899.234, ignore_decimal=False) == \
        '40.08T'
    assert stringify_number(-852656789.23) == '-852M'
    assert stringify_number(-852656789.23, ignore_decimal=False) == '-852.66M'


def test_commafy_number():
    logger.info("Testing " + inspect.stack()[0][3])

    assert commafy_number(12345634) == '12,345,634'
    assert commafy_number(547856789.23) == '547,856,789.23'
    assert commafy_number(547856789.23, ignore_decimal=True) == '547,856,789'
    assert commafy_number(498785643789) == '498,785,643,789'
    assert commafy_number(4007856437895,
                          ignore_decimal=True) == '4,007,856,437,895'
    assert commafy_number(498785643789.123) == '498,785,643,789.12'
    assert commafy_number(4567856437895.90,
                          ignore_decimal=True) == '4,567,856,437,895'
    assert commafy_number(-852656789.23) == '-852,656,789.23'
    assert commafy_number(-852656789.23, ignore_decimal=True) == '-852,656,789'


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