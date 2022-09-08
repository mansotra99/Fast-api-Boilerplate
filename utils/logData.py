import json,os
from pprint import pprint
from loguru import logger
from utils.helpers import current_datetime


from .logging import init_logging

init_logging()


job_dict={}

 
class LogDataClass(object):
    

    def __init__(self ,request_id ) -> None:
        
        self.request_id=request_id
        self.job_dict={
            
            "@fields":{
                'level':"info"
            },
            "@message" :{
                 "request_id":self.request_id,
                 "time":str(current_datetime()),
            }

        }
       
    def log_data(self):
        if os.getenv('ENVIRONMENT')=="DEVELOPMENT":
            pprint(self.job_dict)
        logger.info(self.job_dict)
        
        
        
    def general_log(self,data):
        self.job_dict['data']=data
        self.log_data()
        # self.log.opt(depth=1,colors=True).info(self.job_dict)
    
    def request_log(self,request):
        self.job_dict["@message"].update(dict(request.headers))
        self.job_dict["@message"]['body']=dict(request._form)
        self.job_dict["@message"]['params']=dict(request.query_params)
        self.job_dict["@message"]['url']=str(request.url)
        self.job_dict["@message"]['method']=str(request.method)
        self.log_data()
        
    

    def response_log(self,response):
        self.job_dict["@message"].update(dict(response.headers))
        self.job_dict["@message"]['body']=json.loads(response.body)
        self.job_dict["@message"]['response_status_code']=response.status_code
        self.log_data()
    
    
    def exception_log(self,exception_dict={}):
        self.job_dict['@fields']['level']="Warn"
        self.job_dict['@message'].update(exception_dict)
        self.log_data()

         