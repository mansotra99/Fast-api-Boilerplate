from email import message
import json
from fastapi import APIRouter, Form,Request ,Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from utils.logData import LogDataClass


class CustomResponse(object):
    # status_code: int
    # request : Request
    # responseData : {} 
    
    def __init__(self ,**kwargs ) -> None:
        self.status_code=kwargs.get('status_code')
        self.responseData={
            "message":kwargs.get("message")
        }
        if kwargs.get('data'):
            self.responseData['data']=kwargs.get('data')
        self.request=kwargs.get('request')
    
    def customResp(self):
        response_log={
            "request_id":self.request.state.request_token,
            "data":self.responseData
        }
         
        response=JSONResponse(status_code=self.status_code, content=self.responseData )
        response.set_cookie(key='request_id',value=self.request.state.request_token)     
        LogDataClass(request_id=self.request.state.request_token).response_log(response)               
        return response

def basic_reponse(**kwargs):
    Resp=CustomResponse(kwargs)
    return Resp.customResp()
    

