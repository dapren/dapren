from __future__ import print_function
from __future__ import division
import os
import inspect
import gzip
import constants
from constants import logger

def file_exists(file_name, **args_map):
    return os.path.isfile(file_name)


def silent_remove(file_name):
    try:
        os.remove(file_name)
    except OSError:
        pass


def file2stdout(file_name, **args_map):
    """
    Read a file into list which each corresponding to 1 item
    Keys in args_map
    - from_line: Start reading file from this line
    - to_line: End reading file at this line
    - file_type = ['gz']
    :param file_name:
    :param args_map:
    :return:
    """

    # Process argument map of the method
    __from_line = 1
    if args_map.has_key('from_line'):
        __from_line = args_map.get('from_line')

    __to_line = 100000000  # Max 100 million lines can be read
    if args_map.has_key('to_line'):
        __to_line = args_map.get('to_line')

    __file_type = "txt"
    if file_name.endswith(".gz"):
        __file_type = "gz"

    if args_map.has_key('file_type'):
        __file_type = args_map.get('file_type')


    # Method logic
    line_number = 0
    if __file_type == 'gz':
        with gzip.open(file_name, 'rb') as f:
            for line in f:
                line_number += 1
                if __from_line <= line_number <= __to_line:
                    print(line.strip("\n"))
    else:
        with open(file_name, 'r') as f:
            for line in f:
                line_number += 1
                if __from_line <= line_number <= __to_line:
                    print(line.strip("\n"))


def file2list(file_name, **args_map):
    """
    Read a file into list which each corresponding to 1 item
    Keys in args_map
    - from_line: Start reading file from this line
    - to_line: End reading file at this line
    - file_type = ['gz']
    :param file_name:
    :param args_map:
    :return:
    """

    # Process argument map of the method
    __from_line = 1
    if args_map.has_key('from_line'):
        __from_line = args_map.get('from_line')

    __to_line = 100000000  # Max 100 million lines can be read
    if args_map.has_key('to_line'):
        __to_line = args_map.get('to_line')

    __file_type = "txt"
    if file_name.endswith(".gz"):
        __file_type = "gz"

    if args_map.has_key('file_type'):
        __file_type = args_map.get('file_type')


    # Method logic
    file_data = []
    line_number = 0
    if __file_type == 'gz':
        with gzip.open(file_name, 'rb') as f:
            for line in f:
                line_number += 1
                if __from_line <= line_number <= __to_line:
                    file_data.append(line.strip("\n"))
    else:
        with open(file_name, 'r') as f:
            for line in f:
                line_number += 1
                if __from_line <= line_number <= __to_line:
                    file_data.append(line.strip("\n"))

    return file_data


def list2file(data, file_name, **args_map):
    """
    Write content of list to a file
    Keys in args_maps
    - mode = ['w','a']
    - file_type = ['gz']
    :param data:
    :param filename:
    :param args_maps:
    :return:
    """
    # Process argument map of the method
    __mode = 'w'
    if args_map.has_key('mode'):
        __mode = args_map.get('mode')

    __file_type = "txt"
    if file_name.endswith(".gz"):
        __file_type = "gz"

    if args_map.has_key('file_type'):
        __file_type = args_map.get('file_type')

    # Cannot support append mode in gzip files. Exits in that case
    if __mode == 'a' and __file_type == "gz":
        raise IOError("Gzip files cannot be written in append mode")


    # Implement method logic
    if __file_type == 'gz':
        with gzip.open(file_name, 'wb') as f:
            for line in data:
                f.write(str(line) + "\n")
    else:
        with open(file_name, __mode) as f:
            for line in data:
                f.write(str(line) + "\n")


def str2file(data, file_name, **args_map):
    """
    Writes a string to file
    Keys in args_maps
    - mode = ['w','a']
    - file_type = ['gz']
    :param data:
    :param file_name:
    :param args_map:
    :return:
    """

    # Process argument map of the method
    __mode = 'w'
    if args_map.has_key('mode'):
        __mode = args_map.get('mode')

    __file_type = "txt"
    if file_name.endswith(".gz"):
        __file_type = "gz"

    if args_map.has_key('file_type'):
        __file_type = args_map.get('file_type')


    # Cannot support append mode in gzip files. Exits in that case
    if __mode == 'a' and __file_type == "gz":
        raise IOError("Gzip files cannot be written in append mode")

    # Implement method logic
    if __file_type == 'gz':
        with gzip.open(file_name, 'wb') as f:
            f.write(data + "\n")
    else:
        with open(file_name, __mode) as f:
            f.write(data + "\n")


def number_of_lines(file_name, **args_map):
    """
    Returns the number of lines in a file
    Keys in args_maps
    - stop_after_n_lines: Stop reading file after this line
    :param file_name: File name with absolute path
    :return: Returns number of lines in the file
    """

    # Process argument map of the method
    __stop_after_n_lines = -1
    if args_map.has_key('stop_after_n_lines'):
        __stop_after_n_lines = args_map.get('stop_after_n_lines')

    # Implement method logic
    line_num = 0
    with open(file_name, 'r') as f:
        for line in f:
            line_num += 1
            if line_num == __stop_after_n_lines:
                break

    return line_num


def size_in_bytes(file_name, **args_map):
    return os.stat(file_name).st_size


def size_in_kb(file_name, **args_map):
    return float(format(size_in_bytes(file_name) / 1024, '.2f'))


def size_in_mb(file_name, **args_map):
    return float(format(size_in_bytes(file_name) / 1048576, '.2f'))


def size_in_gb(file_name, **args_map):
    return float(format(size_in_bytes(file_name) / 1073741824, '.2f'))


def size_in_tb(file_name, **args_map):
    return float(format(size_in_bytes(file_name) / 1099511627776, '.2f'))


def is_file_zero_bytes(file_name, **args_map):
    if size_in_bytes(file_name) == 0:
        return True
    else:
        return False

def get_files_in_dir(path, **args_map):
    # returns a list of names (with extension, without full path) of all files
    # in folder path
    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            files.append(name)
    return files


# -----------------------------------------------------------------------------
# ----------------------------------------------------------------- UNIT TESTS
# -----------------------------------------------------------------------------
def test_file_exists():
    logger.info("Testing " + inspect.stack()[0][3])

    assert file_exists(constants.FILENAME_TEST_FILE_OPS_1) == True
    assert file_exists('some_file_that_does_not_exists') == False


def test_silent_remove():
    logger.info("Testing " + inspect.stack()[0][3])
    silent_remove("{I_AM_SURE-THIS_FILE_DOES-NOT_EXISTS}")


def test_is_file_zero_bytes():
    logger.info("Testing " + inspect.stack()[0][3])

    assert is_file_zero_bytes(
        constants.FILENAME_TEST_FILE_OPS_ZERO_BYTE_FILE) == True
    assert is_file_zero_bytes(constants.FILENAME_TEST_FILE_OPS_1) == False


def test_number_of_lines():
    logger.info("Testing " + inspect.stack()[0][3])

    logger.debug(number_of_lines(constants.FILENAME_TEST_FILE_OPS_1))
    logger.debug(number_of_lines(constants.FILENAME_TEST_FILE_OPS_1,
                                  stop_after_n_lines=101))

    assert number_of_lines(constants.FILENAME_TEST_FILE_OPS_1) == 6264
    assert number_of_lines(constants.FILENAME_TEST_FILE_OPS_1,
                           stop_after_n_lines=101) == 101


def test_size_of_file():
    logger.info("Testing " + inspect.stack()[0][3])

    logger.debug(size_in_bytes(constants.FILENAME_TEST_FILE_OPS_1))
    logger.debug(size_in_kb(constants.FILENAME_TEST_FILE_OPS_1))
    logger.debug(size_in_mb(constants.FILENAME_TEST_FILE_OPS_1))

    assert size_in_bytes(
        constants.FILENAME_TEST_FILE_OPS_1) == 428432
    assert size_in_kb(constants.FILENAME_TEST_FILE_OPS_1) == 418.39
    assert size_in_mb(constants.FILENAME_TEST_FILE_OPS_1) == 0.41


def test_file2list():
    logger.info("Testing " + inspect.stack()[0][3])

    actual_data = file2list(
        constants.FILENAME_TEST_FILE_OPS_LOAD_FILE_IN_LIST)
    expected_data = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    assert actual_data == expected_data

    actual_data = file2list(
        constants.FILENAME_TEST_GZIPPED_FILE_OPS_LOAD_FILE_IN_LIST,
        from_line=3, to_line=9)
    expected_data = ['3', '4', '5', '6', '7', '8', '9']
    assert actual_data == expected_data

    data = file2list(
        constants.FILENAME_TEST_FILE_OPS_LOAD_FILE_IN_LIST, from_line=5)
    assert str(data) == "['5', '6', '7', '8', '9', '10']"

    data = file2list(
        constants.FILENAME_TEST_FILE_OPS_LOAD_FILE_IN_LIST, from_line=5,
        to_line=7)
    assert str(data) == "['5', '6', '7']"

    data = file2list(
        constants.FILENAME_TEST_FILE_OPS_LOAD_FILE_IN_LIST, to_line=2)
    assert str(data) == "['1', '2']"


def test_list2file():
    logger.info("Testing " + inspect.stack()[0][3])

    # Test mode = w (default mode)
    data = ['1', '2', '3', '4']
    file_name = constants.DAPREN_TMP_DIR + "/test_list2file.deleteme.txt"
    silent_remove(file_name)

    list2file(data, file_name)
    list2file(data, file_name)

    expected_data = ['1', '2', '3', '4']
    actual_data = file2list(file_name)
    assert expected_data == actual_data

    os.remove(file_name)

    # Test mode = a

    data = ['1', '2', '3', '4']
    file_name = constants.DAPREN_TMP_DIR + "/test_list2file.deleteme.txt"
    silent_remove(file_name)

    list2file(data, file_name, mode='a')

    data = ['5']
    list2file(data, file_name, mode='a')

    expected_data = ['1', '2', '3', '4', '5']
    actual_data = file2list(file_name)

    assert expected_data == actual_data
    os.remove(file_name)

    # Test creation of gzip file without suffix ".gz"
    data = ['1', '2', '3', '4']
    file_name = constants.DAPREN_TMP_DIR + "/test_list2file.gzipped.deleteme.txt"
    silent_remove(file_name)

    list2file(data, file_name, file_type="gz")

    expected_data = ['1', '2', '3', '4']
    actual_data = file2list(file_name, file_type="gz")

    assert expected_data == actual_data
    os.remove(file_name)

    # Test creation of gzip file WITH suffix ".gz"
    data = ['1', '2', '3', '4']
    file_name = constants.DAPREN_TMP_DIR + "/test_list2file.gzipped.deleteme.txt.gz"
    silent_remove(file_name)

    list2file(data, file_name)

    expected_data = ['1', '2', '3', '4']
    actual_data = file2list(file_name)

    assert expected_data == actual_data
    os.remove(file_name)

def test_str2file():
    logger.info("Testing " + inspect.stack()[0][3])

    # Test for mode = 'w'
    data = '1234'
    file_name = constants.DAPREN_TMP_DIR + "/test_str2file.deleteme.txt"
    silent_remove(file_name)

    str2file(data, file_name)

    data = '5678'
    str2file(data, file_name)

    expected_data = ['5678']
    actual_data = file2list(file_name)
    assert expected_data == actual_data

    os.remove(file_name)

    # Test for mode = 'a'
    data = '1234'
    file_name = constants.DAPREN_TMP_DIR + "/test_append_str2file.deleteme.txt"
    silent_remove(file_name)

    str2file(data, file_name, mode='a')

    data = '5678'
    str2file(data, file_name, mode='a')

    expected_data = ['1234', '5678']
    actual_data = file2list(file_name)
    assert expected_data == actual_data

    os.remove(file_name)

    # Test creation of gzip file without suffix ".gz"
    data = '1234'
    file_name = constants.DAPREN_TMP_DIR + "/test_str2file.gzipped.deleteme.txt"
    silent_remove(file_name)

    str2file(data, file_name, file_type="gz")

    expected_data = ['1234']
    actual_data = file2list(file_name, file_type="gz")

    assert expected_data == actual_data
    os.remove(file_name)

    # Test creation of gzip file WITH suffix ".gz"
    data = '1234'
    file_name = constants.DAPREN_TMP_DIR + "/test_str2file.gzipped.deleteme.txt.gz"
    silent_remove(file_name)

    str2file(data, file_name)

    expected_data = ['1234']
    actual_data = file2list(file_name)

    assert expected_data == actual_data
    os.remove(file_name)


# -----------------------------------------------------------------------------
# ----------------------------------------------------------------------- MAIN
# -----------------------------------------------------------------------------
if __name__ == '__main__':

    # Execute all test methods. All test methods should start with string
    # "test_"
    for name in dir():
        if name.startswith("test_"):
            eval(name)()

    logger.info("All tests run fine")