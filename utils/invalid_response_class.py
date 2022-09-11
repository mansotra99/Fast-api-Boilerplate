from cgitb import reset
import json
from utils.logData import LogDataClass
from loguru import logger

class InvalidationException(Exception):
    def __init__(self, name: str):
        self.name = name


class InternalServerError(Exception):
    def __init__(self, exception_dict : dict, request_id : str):
        LogDataClass(request_id).exception_log(exception_dict)
