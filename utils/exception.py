import sys
import traceback
import json
from sentry_sdk import *
from utils.invalid_response_class import InternalServerError


class Exception:
    def __init__(self):
        
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        self.Error_data={
            "exception_type":str(exception_type),
            "exception_object":str(exception_object),
            "exception_traceback":str(traceback.format_exc()),
            "line_number":str(line_number),
            "filename":str(filename),
        }
        with push_scope() as scope:
            scope.set_extra("custom_exp_obj",self.Error_data)
            capture_exception(exception_object)
        
        self.exception_obj={
                "status":500,
                "message":str(exception_object),
                "traceback":str(traceback.format_exc()),
                "Error_Data":self.Error_data,
            }
       
    def raise_exception(self,request_id):
        raise InternalServerError(self.Error_data,request_id)
    
    def return_json(self):
        return json.dumps(self.exception_obj) 

         