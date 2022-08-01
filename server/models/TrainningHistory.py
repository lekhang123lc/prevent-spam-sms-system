from tkinter.ttk import Separator
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import Session
from db import Base
from pydantic import BaseModel
from db import engine
from sqlalchemy import desc
from datetime import datetime
from models.SmsModel import *
import random

class TrainningHistory(Base):
    __tablename__ = "trainning_history"
    # fields 
    id             = Column(Integer,primary_key=True, index=True)
    time_trainning = Column(DateTime)
    p_spam         = Column(Float)
    n_vocabulary   = Column(Integer)
    n_spam_sms     = Column(Integer)
    n_normal_sms   = Column(Integer)
    alpha          = Column(Float)
    p_exactly      = Column(Float)


def add_trainning(db:Session, p_spam:float, n_vocabulary:int, n_spam_sms:int, n_normal_sms:int, alpha=1):
    
    # create message instance 
    new_trainning = TrainningHistory(  p_spam=p_spam, 
                        n_vocabulary=n_vocabulary, 
                        n_spam_sms=n_spam_sms,
                        n_normal_sms=n_normal_sms,
                        alpha=alpha,time_trainning=datetime.now())
    db.add(new_trainning)
    db.commit()
    db.refresh(new_trainning)
    return new_trainning

def get_last_trainning(db:Session):
    return db.query(TrainningHistory).order_by(desc(TrainningHistory.id)).limit(1).first()

def save_trainning(db:Session, trainning_history:TrainningHistory):
    is_trainning_updated = db.query(TrainningHistory).filter(TrainningHistory.id == trainning_history.id).update({
            TrainningHistory.p_spam: trainning_history.p_spam,
            TrainningHistory.p_exactly: trainning_history.p_exactly,
        })
    return is_trainning_updated

def list_trainning(db:Session, page, page_size=30):
    trainnings = db.query(TrainningHistory).order_by(TrainningHistory.id.desc()).limit(page_size).offset((page-1)*page_size).all()
    return trainnings

def get_max_page_trainning(db:Session, page_size=30):
    count = db.query(TrainningHistory).count()
    max_page = int(count)//page_size
    if count%page_size != 0:
        max_page=max_page+1
    return max_page