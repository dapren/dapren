import sqlite3
import constants
import os
from constants import dapren_logger
import inspect
from utilops import guid
import fileops
import bashops
import strops


###############################################################################
def load_data_from_file(
        db_filename=None,
        db_table_to_load=None,
        data_filename=None,
        is_first_row_header=False,
        delimiter=constants.char_tab,
        **kwargs):

    if db_filename is None:
        err_msg = "Parameter 'db_filename' is required"
        raise ValueError(err_msg)

    if data_filename is None:
        err_msg = "Parameter 'data_filename' is required"
        raise ValueError(err_msg)

    if db_table_to_load is None:
        err_msg = "Parameter 'db_table_to_load' is required"
        raise ValueError(err_msg)

    insert_query = __generate_insert_statement(
        db_filename=db_filename,
        db_table_to_load=db_table_to_load)

    data = []
    is_first_line = True
    lines = 0
    for line in fileops.file2list(data_filename):
        if is_first_row_header and is_first_line:
            is_first_line = False
            continue

        data.append(line.split(delimiter))
        lines += 1

    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        cursor.executemany(insert_query, data)

    return lines


def test_load_data_from_file():
    dapren_logger.info("Testing " + inspect.stack()[0][3])

    ############################################################################
    dapren_logger.info("Testing loading of tsv file with no header")
    db_filename = create_test_db_basic()
    load_data_from_file(
        db_filename=db_filename,
        db_table_to_load="Person",
        data_filename=constants.FILENAME_TEST_SQLITE_TABLE_LOAD_IN_TSV,
        )

    actual = []
    for line in execute(
        db_filename=db_filename,
        query="select firstname,age from person"):

        actual.append(line)

    expected = [(u'Amit', 36),
                (u'John', 36),
                (u'Sanjay', 43),
                (u'Tiger', 54),
                (u'Tom', 56),
                ('firstname', 'age')]
    fileops.silent_remove(db_filename)
    assert expected == sorted(actual)

    ############################################################################
    dapren_logger.info("Testing loading of tsv file with header")
    db_filename = create_test_db_basic()
    load_data_from_file(
        db_filename=db_filename,
        db_table_to_load="Person",
        data_filename=constants.FILENAME_TEST_SQLITE_TABLE_LOAD_IN_TSV,
        is_first_row_header=True
        )

    actual = []
    for line in execute(
        db_filename=db_filename,
        query="select firstname,age from person"):

        actual.append(line)

    expected = [(u'John', 36),
                (u'Sanjay', 43),
                (u'Tiger', 54),
                (u'Tom', 56),
                ('firstname', 'age')]
    fileops.silent_remove(db_filename)
    assert expected == sorted(actual)


def __generate_insert_statement(db_filename, db_table_to_load):
    column_list = get_column_list(db_filename=db_filename,
                                  table=db_table_to_load)

    query = """INSERT INTO {} ({}) VALUES ({})""".format(
        db_table_to_load,
        ", ".join(column_list),
        ",".join(list("?" * len(column_list))))

    return query


def test___generate_insert_statement():
    dapren_logger.info("Testing " + inspect.stack()[0][3])

    db_filename = create_test_db_basic()
    expected = "INSERT INTO Person (firstname, lastname, age) VALUES (" \
               "?,?,?)"
    actual = __generate_insert_statement(db_filename, "Person")
    fileops.silent_remove(db_filename)
    assert expected == actual


###############################################################################
def get_table_list(
        db_filename=None,
        **kwargs
    ):

    if db_filename is None:
        err_msg = "Parameter 'db_filename' is required"
        raise ValueError(err_msg)

    query = """SELECT name FROM sqlite_master WHERE type='table'"""

    output_table_list = []
    for qr in execute(
            db_filename=db_filename,
            query=query,
            header_row=False):

        output_table_list.append(qr[0])

    return output_table_list


def test_get_table_list():
    dapren_logger.info("Testing " + inspect.stack()[0][3])
    db_filename = create_test_db_basic()

    expected = [u'Person', u'Product']
    actual = get_table_list(db_filename)
    fileops.silent_remove(db_filename)
    assert expected == actual


###############################################################################
def get_column_list(
        db_filename=None,
        table=None,
        **kwargs
    ):

    if db_filename is None:
        err_msg = "Parameter 'db_filename' is required"
        raise ValueError(err_msg)

    if table is None:
        err_msg = "Parameter 'table' is required"
        raise ValueError(err_msg)

    query = """PRAGMA table_info({})""".format(table)

    output_column_list = []
    for qr in execute(
            db_filename=db_filename,
            query=query,
            header_row=False):

        output_column_list.append(qr[1])

    return output_column_list


def test_get_column_list():
    dapren_logger.info("Testing " + inspect.stack()[0][3])
    db_filename = create_test_db_basic()

    expected = [u'firstname', u'lastname', u'age']
    actual = get_column_list(db_filename, "Person")
    fileops.silent_remove(db_filename)
    assert expected == actual


###############################################################################
def extract_data_to_file(
    db_filename=None,
    query=None,
    header_row=True,
    return_output_as_dict=False,  # If False, we return output as dict
    output_file_name=None,
    append_to_file=False,
    overwrite_file=False,
    output_delimiter=constants.char_tab,
    key_value_delimiter=constants.char_equal,
    key_value_pair_delimiter=constants.char_tab,
    **kwargs
    ):

    if db_filename is None:
        err_msg = "Parameter 'db_filename' is required"
        raise ValueError(err_msg)

    if query is None:
        err_msg = "Parameter 'query' is required"
        raise ValueError(err_msg)

    if output_file_name is None:
        err_msg = "Parameter 'output_file_name' is required"
        raise ValueError(err_msg)

    if not append_to_file \
            and os.path.exists(output_file_name)\
            and not overwrite_file:
        err_msg="""
        File {} already exists. Either provide another file name or s`et flag
        'append_to_file' or 'overwrite_file' to True
        """.format(output_file_name)
        raise IOError(err_msg)

    file_write_mode = "w"
    if append_to_file:
        file_write_mode = "a"

    already_seen_first_line = False
    with open(output_file_name, file_write_mode) as fw:
        if return_output_as_dict:

            for output_dict in execute(
                    db_filename=db_filename,
                    query=query,
                    return_output_as_dict=return_output_as_dict,
                    header_row=header_row):

                output_list = []
                for k, v in output_dict.items():
                    output_list.append("{}{}{}".format(k,
                                                       key_value_delimiter,
                                                       v))

                if already_seen_first_line is False:
                    if append_to_file:
                        fw.write(constants.char_newline)
                    fw.write(key_value_pair_delimiter.join(output_list))
                    already_seen_first_line = True
                else:
                    fw.write(constants.char_newline)
                    fw.write(key_value_pair_delimiter.join(output_list))
        else:
            for output_list in execute(
                    db_filename=db_filename,
                    query=query,
                    return_output_as_dict=return_output_as_dict,
                    header_row=header_row):

                if already_seen_first_line is False:
                    if append_to_file:
                        fw.write(constants.char_newline)

                    fw.write(output_delimiter.join(map(str, output_list)))
                    already_seen_first_line = True
                else:
                    fw.write(constants.char_newline)
                    fw.write(output_delimiter.join(map(str, output_list)))


def test_extract_data_to_file():
    dapren_logger.info("Testing " + inspect.stack()[0][3])

    ############################################################################
    dapren_logger.info("Test dict output to a file")
    db_filename = create_test_db_basic()
    output_file_name = "{}.txt".format(guid())

    extract_data_to_file(
        db_filename=db_filename,
        query="SELECT * FROM person",
        return_output_as_dict=True,  # If False, we return output as dict
        output_file_name=output_file_name,
        append_to_file=False,
        overwrite_file=False,
        key_value_pair_delimiter='&')

    expected = ['lastname=Dash&age=36&firstname=John',
                'lastname=Dyson&age=54&firstname=Tiger',
                'lastname=Sawyer&age=56&firstname=Tom']

    actual = sorted(fileops.file2list(output_file_name))
    fileops.silent_remove(db_filename)
    fileops.silent_remove(output_file_name)

    assert actual == expected

    ############################################################################
    dapren_logger.info("Test list output to a file")
    db_filename = create_test_db_basic()
    output_file_name = "{}.txt".format(guid())

    extract_data_to_file(
        db_filename=db_filename,
        query="SELECT * FROM person",
        output_file_name=output_file_name,
        append_to_file=False,
        overwrite_file=False,
        header_row=False,
        output_delimiter=",")

    expected = ['John,Dash,36', 'Tiger,Dyson,54', 'Tom,Sawyer,56']
    actual = sorted(fileops.file2list(output_file_name))
    fileops.silent_remove(db_filename)
    fileops.silent_remove(output_file_name)

    assert actual == expected

    ############################################################################
    dapren_logger.info("Test 'append_to_file' flag")
    db_filename = create_test_db_basic()
    output_file_name = "{}.txt".format(guid())

    extract_data_to_file(
        db_filename=db_filename,
        query="SELECT * FROM person",
        return_output_as_dict=True,  # If False, we return output as dict
        output_file_name=output_file_name,
        append_to_file=False,
        overwrite_file=False,
        key_value_pair_delimiter='&')

    extract_data_to_file(
        db_filename=db_filename,
        query="SELECT * FROM person",
        return_output_as_dict=True,  # If False, we return output as dict
        output_file_name=output_file_name,
        append_to_file=True,
        overwrite_file=False,
        key_value_pair_delimiter='&')

    expected = ['lastname=Dash&age=36&firstname=John',
                'lastname=Dash&age=36&firstname=John',
                'lastname=Dyson&age=54&firstname=Tiger',
                'lastname=Dyson&age=54&firstname=Tiger',
                'lastname=Sawyer&age=56&firstname=Tom',
                'lastname=Sawyer&age=56&firstname=Tom']

    actual = sorted(fileops.file2list(output_file_name))
    fileops.silent_remove(db_filename)
    fileops.silent_remove(output_file_name)

    assert actual == expected

    ############################################################################
    dapren_logger.info("Test 'overwrite_file' and 'append_to_file' flag")
    db_filename = create_test_db_basic()
    output_file_name = "{}.txt".format(guid())

    extract_data_to_file(
        db_filename=db_filename,
        query="SELECT * FROM person",
        return_output_as_dict=False,  # If False, we return output as dict
        output_file_name=output_file_name,
        append_to_file=False,
        overwrite_file=False,
        key_value_pair_delimiter='&')

    extract_data_to_file(
        db_filename=db_filename,
        query="SELECT * FROM person",
        return_output_as_dict=False,  # If False, we return output as dict
        output_file_name=output_file_name,
        append_to_file=True,
        overwrite_file=True,
        key_value_pair_delimiter='&')

    expected = ['John\tDash\t36',
                'John\tDash\t36',
                'Tiger\tDyson\t54',
                'Tiger\tDyson\t54',
                'Tom\tSawyer\t56',
                'Tom\tSawyer\t56',
                'firstname\tlastname\tage',
                'firstname\tlastname\tage']

    actual = sorted(fileops.file2list(output_file_name))
    fileops.silent_remove(db_filename)
    fileops.silent_remove(output_file_name)

    assert actual == expected


###############################################################################
def execute(
        db_filename=None,
        query=None,
        header_row=True,
        return_output_as_dict=False,  # If False, we return output as dict
        **kwargs
        ):

    if db_filename is None:
        err_msg = "Parameter 'db_filename' is required"
        raise ValueError(err_msg)

    if query is None:
        err_msg = "Parameter 'query' is required"
        raise ValueError(err_msg)

    with sqlite3.connect(db_filename) as conn:
        if return_output_as_dict:
            conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute(query)

        # If output is being returned as dict then no need of header row
        col_names = []
        for colinfo in cursor.description:
            col_names.append(colinfo[0])

        if not return_output_as_dict and header_row:
            yield tuple(col_names)

        for row in cursor.fetchall():
            if return_output_as_dict:

                output_dict = {}
                for index, value in enumerate(col_names):
                    output_dict[value] = row[index]
                yield output_dict
            else:
                yield row


def test_execute():
    dapren_logger.info("Testing " + inspect.stack()[0][3])

    ############################################################################
    dapren_logger.info("Test that select command works and returns list")

    # Load test data
    db_filename = "{}/{}.db".format(constants.DAPREN_TMP_DIR, guid())
    queries = fileops.file2list(constants.FILENAME_TEST_SQLITE_BASIC_SELECT)
    execute_script(
        db_filename=db_filename,
        create_new_db_filename_if_missing=True,
        query="\n".join(queries)
    )

    # Check that data is loaded correctly
    expected = [('firstname', 'lastname', 'age'),
                (u'Tom', u'Sawyer', 56),
                (u'John', u'Dash', 36),
                (u'Tiger', u'Dyson', 54)]
    actual = []
    for result in execute(
        db_filename=db_filename,
        query="SELECT * FROM PERSON",
    ):
        actual.append(result)

    assert str(actual) == str(expected)
    fileops.silent_remove(db_filename)

    ############################################################################
    dapren_logger.info("Test that select command works and returns dict")

    # Load test data
    db_filename = create_test_db_basic()

    # Check that data is loaded correctly
    expected = [u'John', u'Tiger', u'Tom']
    actual = []
    for result in execute(
        db_filename=db_filename,
        query="SELECT * FROM PERSON",
        return_output_as_dict=True
    ):
        actual.append(result['firstname'])
    actual.sort()
    assert str(actual) == str(expected)
    fileops.silent_remove(db_filename)


def create_test_db_basic():
    db_filename = "{}/{}.db".format(constants.DAPREN_TMP_DIR, guid())
    queries = fileops.file2list(constants.FILENAME_TEST_SQLITE_BASIC_SELECT)
    execute_script(
        db_filename=db_filename,
        create_new_db_filename_if_missing=True,
        query="\n".join(queries)
    )
    return db_filename


###############################################################################
def execute_script(
        db_filename=None,
        create_new_db_filename_if_missing=False,
        query=None,
        **kwargs
    ):
    """
    This method is intented to be called when you are running multiple sql
    scripts (like 'create table' statement followed by 'insert table' statement)
    and you just care whether the script ran successfully or not. You do not
    care about the output rows ('select' statements return output hence they
    should NOT be run using this method. Instead they should be run using
    method 'execute'

    :param db_filename: The name of the sqlite db file. Preferrably with
    extention '.db'

    :param create_new_db_filename_if_missing: If the db_filename provided is
    an missing and value of this field is set to True then new file will be
    created else an error will be thrown

    :param query: The query to be executed, delimited by semicolons

    :param kwargs: Not used right now

    :return: Does not returns anything. If the script fails then it result in an
    exception
    """

    # ###################################################### Validate arguments
    if db_filename is None:
        err_message = "Parameter 'db_filename' is required"
        raise ValueError(err_message)

    if query is None:
        err_message = "Parameter 'query' is required"
        raise ValueError(err_message)

    if create_new_db_filename_if_missing is False \
            and not os.path.exists(db_filename):
        err_msg = """
        File '{db_filename}' not found. Please check the name and
        try again. If you want to create a new file then please run this
        method with flag 'create_new_db_filename_if_missing=True'
        """.format(db_filename=db_filename)
        raise IOError(err_msg)

    # ############################################################ Run the query
    with sqlite3.connect(db_filename) as conn:
        dapren_logger.info("About to execute: {}".format(
            strops.make_log_ready(query)))
        conn.executescript(query)
        dapren_logger.info("Executed: {}".format(strops.make_log_ready(query)))


def test_execute_script():
    dapren_logger.info("Testing " + inspect.stack()[0][3])

    ############################################################################
    dapren_logger.info("Test that non existent file throws error w/o correct flags")
    db_filename = "{}.db".format(guid)
    try:
        execute_script(
            db_filename=db_filename,
            query="select 1")
    except IOError:
        pass    # If IOError is thrown then unit test passes
    else:
        assert True is False
    fileops.silent_remove(db_filename)
    ############################################################################
    dapren_logger.info("Test that non existent file does not throws error with  "
                "correct flags")
    db_filename = "{}.db".format(guid())
    try:
        execute_script(
            db_filename=db_filename,
            query="select 1",
            create_new_db_filename_if_missing=True)

        assert True is True

    except IOError:
        assert True is False    # If IOError is thrown then unit test passes
    fileops.silent_remove(db_filename)

    ############################################################################
    dapren_logger.info("Test that valid DDL goes thru fine")

    db_filename = "{0}/{1}.db".format(
        constants.DAPREN_TMP_DIR,
        guid()
        )
    try:
        execute_script(
            db_filename=db_filename,
            create_new_db_filename_if_missing=True,
            query="""
            CREATE TABLE person(firstname string, lastname string, age int);
            INSERT INTO person VALUES ("Dapren", "Python", 1);
            """)

        bashcmd = """
        sqlite3 {} "select * from person"
        """.format(db_filename)

        expected = "Dapren|Python|1\n"
        bash_stdout = bashops.runbash(bashcmd)['stdout']
        actual = bash_stdout[0]
        assert expected == actual

    except sqlite3.OperationalError:
        assert True is False    # If IOError is thrown then unit test has failed
    fileops.silent_remove(db_filename)
    ############################################################################
    dapren_logger.info("Test that invalid DDL fails")

    db_filename = "{0}/{1}.db".format(
        constants.DAPREN_TMP_DIR,
        guid()
        )
    try:
        execute_script(
            db_filename=db_filename,
            create_new_db_filename_if_missing=True,
            query="""
            CREATE TAAABLE person(firstname string, lastname string, age int);
            INSERT INTO person VALUES ("Dapren", "Python", 1)
            """)

        bashcmd = """
        sqlite3 {} "select * from person"
        """.format(db_filename)

        expected = "Dapren|Python|1\n"
        bash_stdout = bashops.runbash(bashcmd)['stdout']
        actual = bash_stdout[0]
        assert expected == actual
        assert True is False    # This line will never be reached
    except sqlite3.OperationalError:
        assert True is True    # If error is thrown then unit test passed
    fileops.silent_remove(db_filename)


# -----------------------------------------------------------------------------
# ----------------------------------------------------------------------- MAIN
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # Execute all test methods. All test methods should start with string
    # "test_"
    for name in dir():
        if name.startswith("test_"):
            eval(name)()

    dapren_logger.info("All tests run fine")


