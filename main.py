
import os,uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse,PlainTextResponse
from db.engine import db
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from middleware.middleware import *

from routers.demo.demo import demoRoute


from utils.invalid_response_class import InternalServerError
from utils.response_manipulator import CustomResponse
from utils.logging import init_logging



if os.getenv('ENVIRONMENT')=="PRODUCTION" or os.getenv('ENVIRONMENT')=="STAGING":

    dsn = os.getenv('DSN')
    sentry_sdk.init(
        dsn= f"{dsn}",

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
        environment=str(os.getenv("ENVIRONMENT"))
    )


app = FastAPI()
app.add_middleware(SentryAsgiMiddleware)




 

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(demoRoute, prefix='/api/fv1/demo', tags=["Demo"],dependencies=[Depends(create_request_id)])

@app.exception_handler(InvalidationException)
async def invalidation_exception_handler(request: Request, exc: InvalidationException):
    return CustomResponse(status_code=401,message=f"Invalid {exc.name}",request=request).customResp()
    
@app.exception_handler(RequestValidationError)
async def handle_error(request: Request, exc: RequestValidationError):
    data=jsonable_encoder(exc.errors())
    return CustomResponse(status_code=400,message=f"Invalid Request",data=data,request=request).customResp()

@app.exception_handler(InternalServerError)
async def internal_server_error(request: Request, exc: InternalServerError):
    return CustomResponse(status_code=400,message="Some Error Occured",request=request).customResp()


init_logging()




@app.get('/ping', tags=['system'])
async def ping():
    return {'ok': 'ok'}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7000,reload=True,workers=4)