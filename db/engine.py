import datetime
from sqlalchemy import create_engine, databases,MetaData,text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
    
Base = declarative_base()

path=os.getenv('ENVIRONMENT')

if path:

    if path=='PRODUCTION':
        os.environ["ENVIRONMENT_PATH"] = '.env.production'
    elif path=='DEVELOPMENT':
        os.environ["ENVIRONMENT_PATH"] = '.env.development'
    elif path=='STAGING':
        os.environ["ENVIRONMENT_PATH"] = '.env.staging'
    else:
        raise RuntimeError('InCorrect  Environment')

    file_path = os.environ["ENVIRONMENT_PATH"]
    isFile = os.path.isfile(file_path) 
    if isFile==False:
        raise RuntimeError(file_path+' file not present')

else:
    raise RuntimeError('Missing  Environment')

load_dotenv(dotenv_path=str(os.getenv('ENVIRONMENT_PATH')))

DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_IP=os.getenv("DB_IP")
DB_NAME=os.getenv("DB_NAME")
DB_PORT=os.getenv("DB_PORT")
SQLALCHEMY_DATABASE_URL_DEV = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_IP}:{DB_PORT}/{DB_NAME}"

ECHO=True
if path=="PRODUCTION":
    ECHO=False

db = create_engine(
    SQLALCHEMY_DATABASE_URL_DEV,echo=ECHO,json_serializer=True, pool_use_lifo=True, pool_pre_ping=True
)

class DbExecute(object):
    def __init__(self) -> None:
        self.engine=db
        self.status=False
        self.data=[]
    
    def del_engine(self):
        del self.engine

    
    def fetchall(self,query,valuelist):
        result=db.execute(text(query),valuelist)
        self.del_engine()
        result=result.mappings().all()
        self.data=result if result else []
        if len(self.data)>0:
            for index,row in enumerate(self.data):
                self.data[index]={column: str(getattr(row, column)) if  isinstance(getattr(row, column), datetime.datetime) else getattr(row, column)   for column in row._keymap.keys()}
            self.status=True
            return self
        else:
            return self
    
    def fetchone(self,query,valuelist):
        result=db.execute(text(query),valuelist)
        self.del_engine()
        result=result.mappings().fetchone()
        self.data=result if result else {}
        if self.data:
            
            self.data={column: str(getattr(self.data, column)) if  isinstance(getattr(self.data, column), datetime.datetime) else getattr(self.data, column)   for column in self.data._keymap.keys()}
            self.status=True
            return self
        else:
            return self
    
    # Function to update fields in a table.
    def update(self,query,valuelist):
        result=db.execute(text(query),valuelist)
        self.del_engine()
        self.status=True
        self.rows_effected = result.rowcount
        return self
  
    # Function to insert single or multiple rows in a table. For single row-entry valueList should be dictonary and for multiple rows-entry valueList should be list containing multiple dictonary.
    def insert(self,query,valuelist):     
        result=db.execute(text(query),valuelist)
        self.del_engine()
        self.status=True
        self.rows_effected = result.rowcount
        return self