from __future__ import print_function
from constants import dapren_logger
import constants
import inspect
import uuid
import dateops


def guid():
    return "{}-{}".format(dateops.date2str(dateops.today(), '%Y%m%d%H'),
                          str(uuid.uuid4()))

def test_guid():
    print (guid())


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