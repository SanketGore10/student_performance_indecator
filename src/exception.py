from src.logger import logging
import sys

def error_message_details(error,error_detail:sys): #custom error handeling fn
    _,_,exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = 'error message: [{0}] line no [{1}] detail [{2}]'.format(
        file_name, exc_tb.tb_lineno, str(error)
    ) 
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys) -> None:  #overriding init method
        super().__init__(error_message, error_detail)  #to inherit the init fn
        self.error_messgae = error_message_details(error_message, error_detail=error_detail) #calling method
    
    def __str__(self) -> str:
        return self.error_messgae
    
# if __name__ == "__main__":
#     try:
#         a=1/0
#     except Exception as e:
#         logging.info("Devide By Zero Exception")
#         raise CustomException(e, sys)