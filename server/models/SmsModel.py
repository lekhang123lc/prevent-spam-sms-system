from tkinter import TRUE
from tkinter.ttk import Separator
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import Session
from db import Base
from pydantic import BaseModel
from db import engine
from sqlalchemy import desc
from fastapi import UploadFile
import pandas as pd

class Message(BaseModel):
    phone_number_send: str
    phone_number_receive: str
    message_status: int
    message_subject: str
    message_content: str
    message_date: str

class SMS_Server(BaseModel):
    phone_number_send: str
    phone_number_receive: str
    message_status: int
    message_subject: str
    message_content: str
    message_date: str
    label: int

# model/table
class SMS(Base):
    __tablename__ = "sms"
    # fields 
    id                   = Column(Integer,primary_key=True, index=True)
    phone_number_send    = Column(String(20))
    phone_number_receive = Column(String(20))
    message_status       = Column(Integer)
    message_subject      = Column(String(255))
    message_content      = Column(String(255))
    message_date         = Column(String(20))
    # label = 0: unknow
    # label = 1: not spam
    # label = 2 : spam
    label                = Column(Integer)

    def isSpam(self):
        return self.label == 2

####################### sms table
def add_sms(db:Session, msg:Message, label:int=0):
    # print(msg)
    # create message instance 
    new_sms = SMS(  phone_number_send=msg.phone_number_send, 
                        phone_number_receive=msg.phone_number_receive, 
                        message_status=msg.message_status, 
                        message_subject=msg.message_subject, 
                        message_content=msg.message_content, 
                        message_date=msg.message_date, 
                        label=label)
    db.add(new_sms)
    db.commit()
    db.refresh(new_sms)
    return new_sms

def update_sms(db:Session, sms:SMS):
    db_sms = get_sms(db=db, id=sms.id)
    db_sms.phone_number_send = sms.phone_number_send
    db_sms.phone_number_receive = sms.phone_number_receive
    db_sms.message_subject = sms.message_subject
    db_sms.message_content = sms.message_content
    db_sms.message_date = sms.message_date
    db_sms.label = sms.label

    db.commit()
    db.refresh(db_sms)
    return TRUE

def get_sms(db:Session, id:int):
    message = db.query(SMS).filter(SMS.id==id).first()
    return message

def list_all_sms(db:Session):
    messages = db.query(SMS).all()
    return messages

def get_max_page(db:Session, page_size=12):
    count = db.query(SMS).count()
    max_page = int(count)//page_size
    if count%page_size != 0:
        max_page=max_page+1
    return max_page

def count_sms(db:Session):
    count = db.query(SMS).count()
    return count

def list_sms(db:Session, page, page_size=12, start=0):
    if start == 0:
        start = (page-1)*page_size
    messages = db.query(SMS).order_by(SMS.id.desc()).limit(page_size).offset(start).all()
    return messages

def clear_all_sms():
    return engine.connect().execute('truncate sms')

def add_list(db, file: UploadFile):
    columns = ['phone_number_send','phone_number_receive','message_status','message_subject', 'message_content', 'message_date', 'label']
    data_xls = pd.read_excel(io=file.file.read(), names = columns)
    n = len(data_xls['message_content'])
    for i in range(n):
        data_msg = Message(  phone_number_send = str(data_xls['phone_number_send'][i]), 
                        phone_number_receive = str(data_xls['phone_number_receive'][i]), 
                        message_status = int(data_xls['message_status'][i]), 
                        message_subject = str(data_xls['message_subject'][i]), 
                        message_content = str(data_xls['message_content'][i]), 
                        message_date = str(data_xls['message_date'][i]))
        # print(type(msg.phone_number_send))
        add_sms(db, data_msg, int(data_xls['label'][i]))
    # print(data_xls['message_content'][0])
    # print(data_xls['message_content'][n-1])
    # data_xls = pd.read_excel(file.file, index_col=None)
    
    # print(data_xls)
    return ""