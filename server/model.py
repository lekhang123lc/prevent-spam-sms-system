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

def get_sms(db:Session, id:int):
    message = db.query(SMS).filter(SMS.id==id).first()
    return message

def list_sms(db:Session):
    messages = db.query(SMS).all()
    return messages

def clear_all_sms():
    return engine.connect().execute('truncate sms')

################# cleaning data
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

############################ /model/table trainning_set_sms

# model/table
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

def isSpam(db:Session, content:String):
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

# model/table
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

def clear_history_trainning():
    return engine.connect().execute('truncate trainning_history')

def add_trainning(db:Session, p_spam:float, n_vocabulary:int, n_spam_sms:int, n_normal_sms:int, alpha=1):
    
    # create message instance 
    new_trainning = TrainningHistory(  p_spam=p_spam, 
                        n_vocabulary=n_vocabulary, 
                        n_spam_sms=n_spam_sms,
                        n_normal_sms=n_normal_sms,
                        alpha=alpha)
    db.add(new_trainning)
    db.commit()
    db.refresh(new_trainning)
    return new_trainning

def trainning(db:Session):
    msg = list_sms(db)
    vocabulary = []
    words = []
    vocabulary_spam_sms = []
    vocabulary_normal_sms = []
    number_word_occurs_spam_sms = {}
    number_word_occurs_normal_sms = {}
    words_spam = 0
    
    for i in msg:
        sentences = split_text_to_word(i.message_content)
        words.append(sentences)

        for word in sentences:
            vocabulary.append(word)
            number_word_occurs_spam_sms.update({word: 0})
            number_word_occurs_normal_sms.update({word: 0})
            if i.isSpam(): 
                vocabulary_spam_sms.append(word)
            else: 
                vocabulary_normal_sms.append(word)
                
    for i in range(len(words)):
        if msg[i].isSpam():
            words_spam+=1 
            for word in words[i]:
                occur = int(number_word_occurs_spam_sms.get(word) or 0)+1
                number_word_occurs_spam_sms.update({word: occur})
        else:
            for word in words[i]:
                occur = int(number_word_occurs_normal_sms.get(word) or 0)+1
                number_word_occurs_normal_sms.update({word: occur})
    clear_old_trainning()
    for word in vocabulary:
        add_word(db, word, int(number_word_occurs_spam_sms.get(word) or 0), int(number_word_occurs_normal_sms.get(word) or 0))
    add_trainning(db, words_spam/len(words), len(vocabulary), len(vocabulary_spam_sms), len(vocabulary_normal_sms))