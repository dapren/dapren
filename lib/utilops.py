from __future__ import print_function
from constants import dapren_logger
import constants
import inspect
"""
This python code kinda implements the toString() of data structures
"""


################################################################################
def str_possible_values(argument_name, list_of_values):
    """
    This is a convieneance method that can be used to display informational
    message above the possible values of an argument

    :param argument_name:
    :param list_of_values:
    :return:
    """
    output_str="Possible value of argument '{}' are".format(argument_name)
    for value in list_of_values:
        output_str += "\n\t- {} ({})".format(value, type(value))

    return output_str


def test_str_possible_values():
    dapren_logger.info("Testing " + inspect.stack()[0][3])
    expected="""Possible value of argument 'WeekendDay' are
	- Sun (<type 'str'>)
	- Sat (<type 'str'>)"""

    actual = str_possible_values("WeekendDay", ['Sun','Sat'])
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

    dapren_logger.info("All tests run fine")