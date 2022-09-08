import random,string
import datetime

def ran_string(size):
	return ''.join(random.choices(string.ascii_letters + string.digits, k = size)) 


def current_datetime():
    # added date time function here so that we won't have import datetime everywhere is needed. Function can directly be imported from here.
    return datetime.datetime.now()