from tkinter.ttk import Separator
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import Session
from db import Base
from pydantic import BaseModel
from db import engine
from sqlalchemy import desc
from models.SmsModel import *
from models.TrainningHistory import *

class TrainningSetSms(Base):
    __tablename__ = "trainning_set_sms"
    # fields 
    id                         = Column(Integer,primary_key=True, index=True)
    word                       = Column(String(255))
    number_occur_in_spam_sms   = Column(String(20))
    number_occur_in_normal_sms = Column(Integer)

def clear_old_trainning():
    return engine.connect().execute('truncate trainning_set_sms')

def add_word(db:Session, word:String, number_occur_in_spam_sms:int, number_occur_in_normal_sms:int):
    
    # create message instance 
    new_word = TrainningSetSms(  word=word, 
                        number_occur_in_spam_sms=number_occur_in_spam_sms, 
                        number_occur_in_normal_sms=number_occur_in_normal_sms)
    db.add(new_word)
    db.commit()
    db.refresh(new_word)
    return new_word

def is_sms_spam(db:Session, content:String):
    words           = split_text_to_word(content)
    trainning_set   = db.query(TrainningSetSms).filter(TrainningSetSms.word.in_(words)).all()
    trainning_value = db.query(TrainningHistory).order_by(desc(TrainningHistory.id)).limit(1).first()
    
    number_word_occurs_spam_sms = {}
    number_word_occurs_normal_sms = {}
    for word in trainning_set:
        number_word_occurs_spam_sms.update({word: word.number_occur_in_spam_sms})
        number_word_occurs_normal_sms.update({word: word.number_occur_in_normal_sms})
    
    p_spam_given_message   = trainning_value.p_spam
    p_ham_given_message    = 1-trainning_value.p_spam
    denominator_spam_sms   = trainning_value.n_spam_sms + trainning_value.alpha*trainning_value.n_vocabulary
    denominator_normal_sms = trainning_value.n_normal_sms + trainning_value.alpha*trainning_value.n_vocabulary
    const = trainning_value.n_vocabulary
    for word in words:
        p_spam_given_message *= const*( float(number_word_occurs_spam_sms.get(word) or 1.0) + trainning_value.alpha)/denominator_spam_sms
        p_ham_given_message  *= const*( float(number_word_occurs_normal_sms.get(word) or 1.0) + trainning_value.alpha)/denominator_normal_sms

    print('P(Spam|message):', p_spam_given_message)
    print('P(Ham|message):', p_ham_given_message)

    if p_ham_given_message > p_spam_given_message:
        print('Label: Ham')
    elif p_ham_given_message < p_spam_given_message:
        print('Label: Spam')
    else:
        print('Equal proabilities, have a human classify this!')
    return p_ham_given_message < p_spam_given_message

def split_text_to_word(s: str):
    separator = ['.', ',', '?', '!']
    sentences = s.lower()
    for i in separator:
        sentences = sentences.replace(i, " ")
    all_words = sentences.split()
    meaning_words = []
    for word in all_words:
        if ( len(word) >= 3 ): meaning_words.append(word)
    return meaning_words

def check_run():
    return 123