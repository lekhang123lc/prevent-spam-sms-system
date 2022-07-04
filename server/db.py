from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#define connection url
DATABASE_URL = "mysql://dev:123123@192.168.56.10/project_sms"

# create new engine instance 
engine = create_engine(DATABASE_URL)

# create sessionmaker 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()