"""
This module contains most commonly used file operations
"""
from __future__ import print_function
from __future__ import division
import os
import inspect
import gzip
import constants
from constants import dapren_logger


def file_exists(file_name, **kwargs):
    """
    :param file_name: Absolute path to filename
    :param kwargs: N/A
    :return: Returns boolean true if file exists else false
    """
    return os.path.isfile(file_name)


def silent_remove(file_name):
    """
    Remove file from disk if exists. If the file does not exits then just exit
    without throwing any exceptions

    :param file_name: Absolute path to filename
    :return: Returns "None"
    """
    try:
        os.remove(file_name)
    except OSError:
        pass


def file2stdout(file_name, **kwargs):
    """
    Writes file to stdout
    :param file_name: Absolute path of input filename
    :param kwargs: Keys in kwargs
    - from_line: Start writing file from this line onwards (inclusive).
    - to_line: End reading file at this line (inclusive)
    - is_gzipped: Possible values: Boolean True or False
    """

    # Process argument map of the method
    __from_line = kwargs.get(constants.str_from_line, 1)
    __to_line = kwargs.get(constants.str_to_line, 10000000000000000L)
    __is_gzipped = kwargs.get(constants.is_gzipped, False)

    # Method logic
    line_number = 0
    if __is_gzipped:
        with gzip.open(file_name, 'rb') as f:
            for line in f:
                line_number += 1
                if __from_line <= line_number <= __to_line:
                    print(line.strip(constants.char_newline))
                elif line_number > __to_line:
                    break
    else:
        with open(file_name, 'r') as f:
            for line in f:
                line_number += 1
                if __from_line <= line_number <= __to_line:
                    print(line.strip(constants.char_newline))
                elif line_number > __to_line:
                    break


def file2list(file_name, **kwargs):
    """
    Read a file into list which each line corresponding to 1 element in list
    :param file_name: Absolute path of input filename
    :param kwargs: Keys in kwargs
    - from_line: Start writing file from this line onwards (inclusive).
    - to_line: End reading file at this line (inclusive)
    - is_gzipped: Possible values: Boolean True or False
    :return List containing all lines between from_line to to_line
    """

    # Process argument map of the method
    __from_line = kwargs.get(constants.str_from_line, 1)
    __to_line = kwargs.get(constants.str_to_line, 10000000000000000L)
    __is_gzipped = kwargs.get(constants.str_is_gzipped, None)

    # Method logic
    file_data = []
    line_number = 0
    if __is_gzipped:
        with gzip.open(file_name, 'rb') as f:
            for line in f:
                line_number += 1
                if __from_line <= line_number <= __to_line:
                    file_data.append(line.strip("\n"))
                elif line_number > __to_line:
                    break
    else:
        with open(file_name, 'r') as f:
            for line in f:
                line_number += 1
                if __from_line <= line_number <= __to_line:
                    file_data.append(line.strip("\n"))
                elif line_number > __to_line:
                    break

    return file_data


def list2file(list_to_output, file_name, **kwargs):
    """
    Write content of list to a file. 1 line per list item

    :param list_to_output:
    :param filename: Absolute path of the filename to which list contents
    need to be copied
    :param kwargs: Keys in kwargs
        - mode = ['w','a']
        - is_gzipped: Possible values: Boolean True or False
    :return: None
    """

    # Process argument map of the method
    __mode = kwargs.get(constants.str_mode, constants.str_w)
    __is_gzipped = kwargs.get(constants.str_is_gzipped, None)

    # Cannot support append mode in gzip files. Exits in that case
    if __mode == 'a' and __is_gzipped:
        raise IOError("Gzip files cannot be written in append mode")

    # Implement method logic
    if __is_gzipped:
        with gzip.open(file_name, constants.str_wb) as f:
            for line in list_to_output:
                f.write(str(line) + constants.char_newline)
    else:
        with open(file_name, __mode) as f:
            for line in list_to_output:
                f.write(str(line) + constants.char_newline)


def str2file(data, file_name, **kwargs):
    """
    Write string data to a file.

    :param data: String data that needs to written to file
    :param filename: Absolute path of the filename to which string
    need to be copied
    :param kwargs: Keys in kwargs
        - mode = ['w','a']
        - is_gzipped: Possible values: Boolean True or False
    :return: None
    """

    # Process argument map of the method
    __mode = kwargs.get(constants.str_mode, constants.str_w)
    __is_gzipped = kwargs.get(constants.str_is_gzipped, None)

    # Cannot support append mode in gzip files. Exits in that case
    if __mode == constants.str_a and __is_gzipped:
        raise IOError("Gzip files cannot be written in append mode")

    # Implement method logic
    if __is_gzipped:
        with gzip.open(file_name, constants.str_wb) as f:
            f.write(data + constants.char_newline)
    else:
        with open(file_name, __mode) as f:
            f.write(data + constants.char_newline)


def number_of_lines(file_name, **kwargs):
    """
    Returns the number of lines in a file
    :param file_name:
    :param kwargs: Keys in kwargs
    - stop_after_n_lines: Stop reading file after this line
    :return: Returns number of lines in the file
    """

    # Process argument map of the method
    __stop_after_n_lines = kwargs.get('stop_after_n_lines', -1)

    # Implement method logic
    line_num = 0
    with open(file_name, 'r') as f:
        for line in f:
            line_num += 1
            if line_num == __stop_after_n_lines:
                break

    return line_num


def size_in_bytes(file_name, **kwargs):
    """
    Return size of file in bytes
    :param file_name: Absolute path to file
    :param kwargs: None
    :return: Return size of file in bytes
    """
    return os.stat(file_name).st_size


def size_in_kb(file_name, **kwargs):
    """
    Return size of file in kb
    :param file_name: Absolute path to file
    :param kwargs: None
    :return: Return size of file in kb
    """
    return float(format(size_in_bytes(file_name) / 1024, '.2f'))


def size_in_mb(file_name, **kwargs):
    """
    Return size of file in mb
    :param file_name: Absolute path to file
    :param kwargs: None
    :return: Return size of file in mb
    """
    return float(format(size_in_bytes(file_name) / 1048576, '.2f'))


def size_in_gb(file_name, **kwargs):
    """
    Return size of file in gb
    :param file_name: Absolute path to file
    :param kwargs: None
    :return: Return size of file in gb
    """

    return float(format(size_in_bytes(file_name) / 1073741824, '.2f'))


def size_in_tb(file_name, **kwargs):
    """
    Return size of file in tb
    :param file_name: Absolute path to file
    :param kwargs: None
    :return: Return size of file in tb
    """
    return float(format(size_in_bytes(file_name) / 1099511627776, '.2f'))


def size_in_pb(file_name, **kwargs):
    """
    Return size of file in tb
    :param file_name: Absolute path to file
    :param kwargs: None
    :return: Return size of file in tb
    """
    return float(format(size_in_bytes(file_name) / 1125899906842624, '.2f'))


def size_adjust_unit(file_name, **kwargs):
    """
    Auto adjusts the unit of file size to kb, mb, gb, tb and pb.
    :param file_name: Absolute path to file
    :param kwargs: None
    :return: Returns a tuple with 2 elements. 1st element in number and 2nd
    element is the unit
    """
    if size_in_kb(file_name) < 1:
        return size_in_bytes(file_name), "bytes"

    elif size_in_mb(file_name) < 1:
        return size_in_kb(file_name), "kb"

    elif size_in_gb(file_name) < 1:
        return size_in_mb(file_name), "mb"

    elif size_in_tb(file_name) < 1:
        return size_in_gb(file_name), "gb"

    elif size_in_pb(file_name) < 1:
        return size_in_tb(file_name), "tb"

    else:
        return size_in_tb(file_name), "pb"


def is_file_zero_bytes(file_name, **kwargs):
    """
    Returns true if file is zero bytes
    :param file_name: Absolute path to file
    :param kwargs: None
    :return: Returns true if file is zero bytes
    """
    if size_in_bytes(file_name) == 0:
        return True
    else:
        return False


def get_files_in_dir(path, **kwargs):
    """
    Returns a list (with extension, without full path) of all files
    in folder path

    :param path: Absolute path to directory
    :param kwargs: None
    """

    files = []
    for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path, filename)):
            files.append(filename)
    return files


def get_dir_in_dir(path, **kwargs):
    """
    Returns a list (with extension, without full path) of all directories
    in folder path

    :param path: Absolute path to directory
    :param kwargs: None
    """

    files = []
    for filename in os.listdir(path):
        if not os.path.isfile(os.path.join(path, filename)):
            files.append(filename)
    return files



# -----------------------------------------------------------------------------
# ----------------------------------------------------------------- UNIT TESTS
# -----------------------------------------------------------------------------
def test_file_exists():
    dapren_logger.info("Testing " + inspect.stack()[0][3])

    assert file_exists(constants.FILENAME_TEST_FILE_OPS_1) == True
    assert file_exists('some_file_that_does_not_exists') == False


def test_silent_remove():
    dapren_logger.info("Testing " + inspect.stack()[0][3])
    silent_remove("{I_AM_SURE-THIS_FILE_DOES-NOT_EXISTS}")


def test_is_file_zero_bytes():
    dapren_logger.info("Testing " + inspect.stack()[0][3])

    assert is_file_zero_bytes(
        constants.FILENAME_TEST_FILE_OPS_ZERO_BYTE_FILE) == True
    assert is_file_zero_bytes(constants.FILENAME_TEST_FILE_OPS_1) == False


def test_number_of_lines():
    dapren_logger.info("Testing " + inspect.stack()[0][3])

    dapren_logger.debug(number_of_lines(constants.FILENAME_TEST_FILE_OPS_1))
    dapren_logger.debug(number_of_lines(constants.FILENAME_TEST_FILE_OPS_1,
                                  stop_after_n_lines=101))

    assert number_of_lines(constants.FILENAME_TEST_FILE_OPS_1) == 6264
    assert number_of_lines(constants.FILENAME_TEST_FILE_OPS_1,
                           stop_after_n_lines=101) == 101


def test_size_of_file():
    dapren_logger.info("Testing " + inspect.stack()[0][3])

    dapren_logger.debug(size_in_bytes(constants.FILENAME_TEST_FILE_OPS_1))
    dapren_logger.debug(size_in_kb(constants.FILENAME_TEST_FILE_OPS_1))
    dapren_logger.debug(size_in_mb(constants.FILENAME_TEST_FILE_OPS_1))

    assert size_in_bytes(
        constants.FILENAME_TEST_FILE_OPS_1) == 428432
    assert size_in_kb(constants.FILENAME_TEST_FILE_OPS_1) == 418.39
    assert size_in_mb(constants.FILENAME_TEST_FILE_OPS_1) == 0.41


def test_file2list():
    dapren_logger.info("Testing " + inspect.stack()[0][3])

    actual_data = file2list(
        constants.FILENAME_TEST_FILE_OPS_LOAD_FILE_IN_LIST)
    expected_data = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    assert actual_data == expected_data

    actual_data = file2list(
        constants.FILENAME_TEST_GZIPPED_FILE_OPS_LOAD_FILE_IN_LIST,
        from_line=3, to_line=9, is_gzipped=True)
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
    dapren_logger.info("Testing " + inspect.stack()[0][3])

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
    dapren_logger.info("Testing " + inspect.stack()[0][3])

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
if __name__ == constants.str___main__:

    # Execute all test methods. All test methods should start with string
    # "test_"
    for name in dir():
        if name.startswith("test_"):
            eval(name)()

    dapren_logger.info("All tests run fine")