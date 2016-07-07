import sqlite3
import constants
import os
from constants import dapren_logger
import inspect
import uuid
import fileops
import bashops
import strops

###############################################################################
def load_data_from_file(
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


###############################################################################
def extract_data_to_file():
    pass


###############################################################################
def execute(
        db_filename=None,
        query=None
        ):

    __validate_args_execute(
        db_filename=db_filename,
        query=query)

    with sqlite3.connect(db_filename) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM person
        """)

        for colinfo in cursor.description:
            print colinfo
        #for row in cursor.fetchall():
        #    row['age']



def __validate_args_execute(
        db_filename,
        query
        ):
    """
    This method runs all validation tests on all arguments for function
    execute
    :param db_filename:
    :param query:
    :return:
    """
    if db_filename is None:
        err_message = "Parameter 'db_filename' is required"
        raise ValueError(err_message)

    if query is None:
        err_message = "Parameter 'query' is required"
        raise ValueError(err_message)

    if not os.path.exists(db_filename):
        err_msg = """
        File '{db_filename}' not found. Please check the name and
        try again.
        """.format(db_filename=db_filename)
        raise IOError(err_msg)


def test_execute():
    dapren_logger.info("Testing " + inspect.stack()[0][3])

    ############################################################################
    dapren_logger.info("Test that non existent file throws error")
    db_filename = "{}.db".format(str(uuid.uuid4()))
    try:
        execute(
            db_filename=db_filename,
            query="select 1")
    except IOError:
        pass    # If IOError is thrown then unit test passes
    else:
        assert True is False

    ############################################################################
    dapren_logger.info("Test that select command works")
    # Load test data
    db_filename = "{}/{}.db".format(constants.DAPREN_TMP_DIR, str(uuid.uuid4()))
    queries = fileops.file2list(constants.FILENAME_TEST_SQLITE_BASIC_SELECT)
    execute_script(
        db_filename=db_filename,
        create_new_db_filename_if_missing=True,
        query="\n".join(queries)
    )

    # Check loaded data
    execute(
        db_filename=db_filename,
        query="SELECT * FROM PERSON"
    )



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
    __validate_args_execute_script(
        db_filename=db_filename,
        query=query,
        create_new_db_filename_if_missing=create_new_db_filename_if_missing
    )

    # Run the query
    with sqlite3.connect(db_filename) as conn:
        dapren_logger.info("About to execute: {}".format(strops.make_log_ready(query)))
        conn.executescript(query)
        dapren_logger.info("Executed: {}".format(strops.make_log_ready(query)))


def __validate_args_execute_script(
        db_filename,
        create_new_db_filename_if_missing,
        query
        ):
    """
    This method runs all validation tests on all arguments for function
    execute_script
    :param db_filename:
    :param query:
    :return:
    """
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


def test_execute_script():
    dapren_logger.info("Testing " + inspect.stack()[0][3])

    ############################################################################
    dapren_logger.info("Test that non existent file throws error w/o correct flags")
    db_filename = "{}.db".format(str(uuid.uuid4()))
    try:
        execute_script(
            db_filename=db_filename,
            query="select 1")
    except IOError:
        pass    # If IOError is thrown then unit test passes
    else:
        assert True is False

    ############################################################################
    dapren_logger.info("Test that non existent file does not throws error with  "
                "correct flags")
    db_filename = "{}.db".format(str(uuid.uuid4()))
    try:
        execute_script(
            db_filename=db_filename,
            query="select 1",
            create_new_db_filename_if_missing=True)

        assert True is True

        fileops.silent_remove(db_filename)
    except IOError:
        assert True is False    # If IOError is thrown then unit test passes

    ############################################################################
    dapren_logger.info("Test that valid DDL goes thru fine")

    db_filename = "{0}/{1}.db".format(
        constants.DAPREN_TMP_DIR,
        str(uuid.uuid4())
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
        fileops.silent_remove(db_filename)
    except sqlite3.OperationalError:
        assert True is False    # If IOError is thrown then unit test has failed

    ############################################################################
    dapren_logger.info("Test that invalid DDL fails")

    db_filename = "{0}/{1}.db".format(
        constants.DAPREN_TMP_DIR,
        str(uuid.uuid4())
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
        fileops.silent_remove(db_filename)
        assert True is False    # This line will never be reached
    except sqlite3.OperationalError:
        assert True is True    # If error is thrown then unit test passed

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


