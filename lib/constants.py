import logging

APPLICATION_LOG_LEVEL = logging.INFO

###############################################################################
# Directory Names
###############################################################################
RESOURCE_DIR = "../resources"
DATA_DIR = "../var/data"
DB_DIR = "../var/db"
INTERIM_DIR = "../var/interim"
LOGS_DIR = "../var/logs"
OUTPUT_DIR = "../var/output"
TMP_DIR = "../var/tmp"


###############################################################################
# File Names
###############################################################################
MODULE_NAME = "unit_tests"

__DIR = RESOURCE_DIR + "/" + MODULE_NAME + "/"

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
