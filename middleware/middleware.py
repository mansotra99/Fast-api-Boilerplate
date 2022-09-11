
from ast import literal_eval
from pprint import pprint
from sqlalchemy import text
import json
import uuid
from fastapi import Depends, FastAPI, Header,Request
from db.engine import db 

from utils.invalid_response_class import InvalidationException
from utils.logData import LogDataClass

exclude_auth={
    "users/sdk/auth":"API",
}

def authenticate_user(request: Request):
    input=[]
    
    headers_params=request.headers

    api_url=str(request.url).split('fv1/')[1]
    
    auth_verification=exclude_auth.get(api_url)
    if auth_verification=="API":
        api_key=headers_params.get('X-api-key')
        
        if api_key:
            # mysql=db.connection()
            result=db.execute(text("""select * from enterprise_account where api_key= :api_key  """),api_key=api_key).fetchone()
            if result:
                request.state.enterprise_data=result._mapping
            else:
                raise InvalidationException("X-api-key")
        else:
            raise InvalidationException("X-api-key")
    elif auth_verification:
        request.state.enterprise_data=[]
        request.state.user_data=[]
    else:
        auth_key=headers_params.get('bearer-token')
         
        if auth_key:
            # mysql=db.connection()
            result=db.execute(text("""select user_id,enterprise_id,email_id,user_name,contact_no from enterprise_users_account where sso_token= :auth_key or secret_key= :secret_key  """),auth_key=auth_key,secret_key=auth_key).fetchone()
            if result:
                request.state.user_data=result._mapping
            else:
                raise InvalidationException("Auth_key")
        else:
            raise InvalidationException("Auth_key")
        


def create_request_id(request: Request):
    request_id=request._headers.get('X-Request-ID')

    
    if request_id:
        request.state.request_token=str(request_id)
    else:
        request_id=str(uuid.uuid4())
        request.state.request_token=request_id
    LogDataClass(request_id=request_id).request_log(request)               

        
        
