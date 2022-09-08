from fastapi import APIRouter, Form,Request,File

from utils.invalid_response_class import InternalServerError
from utils.response_manipulator import CustomResponse
from utils.exception import Exception



demoRoute = APIRouter()

@demoRoute.post('/demo')
def demo(request: Request):
    try:
        # Dummy Response
        data={
            "resp":"Success" 
        }
        return CustomResponse(status_code=200, data=data, message="Success", request=request).customResp()
        
    except:
        raise Exception().raise_exception(request_id=request.state.request_token)
       
