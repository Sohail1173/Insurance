import os,sys

class CustomException(Exception):

    def __init__(self,error_message:Exception,error_detail:sys):
        super().__init__(error_message)
        self.error_messae=CustomException.error_message_detail(error_message,error_detail=error_detail)
@staticmethod
def error_message_detail(error:Exception,error_details:sys)->str:
    
    _,_,exc_tb=error_details.exc_info()
    line_number=exc_tb.tb_frame.f_lineno

    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message=f"error ocucured python script name [{file_name}]" \
    f"line number [{exc_tb.tb_lineno}] error message [{error}]."

    return error_message


def __str__(self):
    """
    Formating how a object should be visible if used in print statements
    .
    """
    return self.error_messae

def __repr__(self):

    """
    Formating object of AppException
    """
    return CustomException