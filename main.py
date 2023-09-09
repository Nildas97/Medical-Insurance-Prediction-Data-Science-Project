# importing libraries
from Insurance.logger import logging
from Insurance.exception import InsuranceException
import os, sys


# defining the test_logger_and_exception function
def test_logger_and_exception():
    try:
        logging.debug("Starting point of the test_logger_and_exception")
        result = 3 / 0
        print(result)
        logging.debug("Ending point of the test_logger_and_exception")
    except Exception as e:
        logging.debug(str(e))
        raise InsuranceException(e, sys)


# calling name function
if __name__ == "__main__":
    try:
        test_logger_and_exception()
    except Exception as e:
        print(e)
