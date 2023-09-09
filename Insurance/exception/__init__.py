# importing libraries
import os, sys


# creating InsuranceException class
class InsuranceException(Exception):
    """
    Description: Returns exceptions details
    Args:
        Exception (str): exception handling

    Returns:
        str: returns exception
    """

    # creating init function for error_message and error_details
    def __init__(self, error_message: Exception, error_detail: sys):
        # creating super class for calling error_message
        super().__init__(error_message)
        self.error_message = InsuranceException.error_message_detail(
            error_message, error_details=error_detail
        )

    @staticmethod
    # defining error_message_detail function
    def error_message_detail(error: Exception, error_details: sys) -> str:
        """
        Description:
            Returns error message details
        Args:
            error (Exception): error types and
            error_details (sys): error line number and file name

        Returns:
            str: returns error message with error details
        """
        # empty function for error_details executable info
        _, _, exc_tb = error_details.exc_info()

        # getting error_message line number
        line_number = exc_tb.tb_frame.f_lineno

        # extract error_message file name
        file_name = exc_tb.tb_frame.f_code.co_filename

        # storing error_message
        error_message = (
            f"error occured python script name [{file_name}]"
            f"line number [{exc_tb.tb_lineno}] error message [{error}]."
        )

        return error_message

    # defining str function
    def __str__(self):
        return InsuranceException.__name__.__str__()
