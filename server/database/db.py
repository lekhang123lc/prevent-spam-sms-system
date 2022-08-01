from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

MYSQL_URL = "mysql://dev:123123@192.168.56.10/project_sms"
POOL_SIZE = 20
POOL_RECYCLE = 3600
POOL_TIMEOUT = 15
MAX_OVERFLOW = 2
CONNECT_TIMEOUT = 60

class Database():
    def __init__(self) -> None:
        self.connection_is_active = False
        self.engine = None

    def get_db_connection(self):
        if self.connection_is_active == False:
            connect_args = {"connect_timeout":CONNECT_TIMEOUT}
            try:
                self.engine = create_engine(MYSQL_URL, pool_size=POOL_SIZE, pool_recycle=POOL_RECYCLE,
                        pool_timeout=POOL_TIMEOUT, max_overflow=MAX_OVERFLOW, connect_args=connect_args)
                return self.engine
            except Exception as ex:
                print("Error connecting to DB : ", ex)
        return self.engine

    def get_db_session(self,engine):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            return session
        except Exception as ex:
            print("Error getting DB session : ", ex)
            return None

app = FastAPI()
app.mount("/views", StaticFiles(directory="views"), name="views")
templates = Jinja2Templates(directory="views")
