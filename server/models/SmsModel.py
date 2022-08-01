from tkinter.ttk import Separator
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import Session
from db import Base
from pydantic import BaseModel
from db import engine
from sqlalchemy import desc

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
    is_sms_updated = db.query(SMS).filter(SMS.id == sms.id).update({
            SMS.phone_number_send: sms.phone_number_send, SMS.phone_number_receive: sms.phone_number_receive,
            SMS.message_subject: sms.message_subject,
            SMS.message_content: sms.message_content,
            SMS.message_date: sms.message_date,
            SMS.label: sms.label
        })
    return is_sms_updated

def get_sms(db:Session, id:int):
    message = db.query(SMS).filter(SMS.id==id).first()
    return message

def list_all_sms(db:Session):
    messages = db.query(SMS).all()
    return messages

def get_max_page(db:Session, page_size=30):
    count = db.query(SMS).count()
    max_page = int(count)//page_size
    if count%page_size != 0:
        max_page=max_page+1
    return max_page

def count_sms(db:Session):
    count = db.query(SMS).count()
    return count

def list_sms(db:Session, page, page_size=30, start=0):
    if start == 0:
        start = (page-1)*page_size
    messages = db.query(SMS).limit(page_size).offset(start).all()
    return messages

def clear_all_sms():
    return engine.connect().execute('truncate sms')