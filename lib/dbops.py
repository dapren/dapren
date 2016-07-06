import sqlite3
import constants
import os
from constants import logger
import inspect
import uuid
import fileops
import bashops

def file2sqlite(
        input_data_filename=None,
        input_delimiter=constants.char_tab,
        db_filename=None,
        db_table_to_load=None,
        create_new_db_filename_if_missing=False,
        create_new_table_to_load_if_missing=False,
        is_first_row_header=True,
        **kwargs
        ):
    pass


def sqlite2file():
    pass


def sqlite_execute_ddl(
        db_filename=None,
        create_new_db_filename_if_missing=False,
        query=None,
        **kwargs
        ):

    __validate_sqlite_execute_ddl(
        db_filename,
        query
        )

    if create_new_db_filename_if_missing is False \
            and not os.path.exists(db_filename):
        err_msg = """
        File '{db_filename}' not found. Please check the name and
        try again. If you want to create a new file then please run this
        method with flag 'create_new_db_filename_if_missing=True'
        """.format(db_filename=db_filename)
        raise IOError(err_msg)

    # Run the query
    with sqlite3.connect(db_filename) as conn:
        conn.executescript(query)


def __validate_sqlite_execute_ddl(
        db_filename,
        query
        ):

    if db_filename is None:
        err_message = "Parameter 'db_filename' is required"
        raise ValueError(err_message)

    if query is None:
        err_message = "Parameter 'query' is required"
        raise ValueError(err_message)


def test_sqlite_execute_ddl():
    logger.info("Testing " + inspect.stack()[0][3])

    ############################################################################
    logger.info("Test that non existent file throws error w/o correct flags")
    db_filename = "{}.db".format(str(uuid.uuid4()))
    try:
        sqlite_execute_ddl(
            db_filename=db_filename,
            query="select 1")
    except IOError:
        pass    # If IOError is thrown then unit test passes
    else:
        assert True is False

    ############################################################################
    logger.info("Test that non existent file does not throws error with  "
                "correct flags")
    db_filename = "{}.db".format(str(uuid.uuid4()))
    try:
        sqlite_execute_ddl(
            db_filename=db_filename,
            query="select 1",
            create_new_db_filename_if_missing=True)

        assert True is True

        fileops.silent_remove(db_filename)
    except IOError:
        assert True is False    # If IOError is thrown then unit test passes

    ############################################################################
    logger.info("Test that valid DDL goes thru fine")

    db_filename = "{0}/{1}.db".format(
        constants.DAPREN_TMP_DIR,
        str(uuid.uuid4())
        )
    try:
        sqlite_execute_ddl(
            db_filename=db_filename,
            create_new_db_filename_if_missing=True,
            query="""
            CREATE TABLE person(firstname string, lastname string, age int);
            INSERT INTO person VALUES ("Dapren", "Python", 1)
            """)

        bashcmd = """
        sqlite3 {} "select * from person"
        """.format(db_filename)

        expected = "Dapren|Python|1\n"
        bash_stdout = bashops.runbash(bashcmd)['stdout']
        actual = bash_stdout[0]
        assert expected == actual
        fileops.silent_remove(db_filename)
    except sqlite3.OperationalError:
        assert True is False    # If IOError is thrown then unit test has failed

    ############################################################################
    logger.info("Test that invalid DDL fails")

    db_filename = "{0}/{1}.db".format(
        constants.DAPREN_TMP_DIR,
        str(uuid.uuid4())
        )
    try:
        sqlite_execute_ddl(
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
        fileops.silent_remove(db_filename)
        assert True is False    # This line will never be reached
    except sqlite3.OperationalError:
        assert True is True    # If error is thrown then unit test passed

if __name__ == "__main__":
    # Execute all test methods. All test methods should start with string
    # "test_"
    for name in dir():
        if name.startswith("test_"):
            eval(name)()

    logger.info("All tests run fine")


