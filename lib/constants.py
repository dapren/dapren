from __future__ import print_function
import logging
import os
APPLICATION_LOG_LEVEL = logging.INFO

###############################################################################
# Directory Names
###############################################################################
if "DAPREN_HOME" in os.environ:
    DAPREN_HOME = os.environ["DAPREN_HOME"]
else:
    DAPREN_HOME = ".."

DAPREN_RESOURCE_DIR = "{}/resources".format(DAPREN_HOME)
DAPREN_DATA_DIR = "{}/var/data".format(DAPREN_HOME)
DAPREN_DB_DIR = "{}/var/db".format(DAPREN_HOME)
DAPREN_INTERIM_DIR = "{}/var/interim".format(DAPREN_HOME)
DAPREN_LOGS_DIR = "{}/var/logs".format(DAPREN_HOME)
DAPREN_OUTPUT_DIR = "{}/var/output".format(DAPREN_HOME)
DAPREN_TMP_DIR = "{}/var/tmp".format(DAPREN_HOME)


###############################################################################
# File Names
###############################################################################
MODULE_NAME = "unit_tests"

__DIR = DAPREN_RESOURCE_DIR + "/" + MODULE_NAME + "/"

__FILE = "test_file_ops_1.txt"
FILENAME_TEST_FILE_OPS_1 = __DIR + __FILE

__FILE = "test_file_ops_zero_byte_file.txt"
FILENAME_TEST_FILE_OPS_ZERO_BYTE_FILE = __DIR + __FILE

__FILE = "test_file_ops_load_file_in_list.txt"
FILENAME_TEST_FILE_OPS_LOAD_FILE_IN_LIST = __DIR + __FILE

__FILE = "test_gzipped_file_ops_load_file_in_list.txt.gz"
FILENAME_TEST_GZIPPED_FILE_OPS_LOAD_FILE_IN_LIST = __DIR + __FILE

###############################################################################
# Strings
###############################################################################
STR_YES = "yes"
STR_NO = "no"

###############################################################################
# Numbers
###############################################################################

###############################################################################
# List
###############################################################################

###############################################################################
# Dict
###############################################################################


if __name__ == '__main__':
    for name in dir():
        evaluated_value = eval(name)
        print ('{name}="{evaluated_value}" ({type})'.format(
            name=name,
            evaluated_value=evaluated_value,
            type=type(evaluated_value)
        ))