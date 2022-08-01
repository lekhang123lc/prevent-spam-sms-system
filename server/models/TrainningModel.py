from tkinter.ttk import Separator
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import Session
from db import Base
from pydantic import BaseModel
from db import engine
from sqlalchemy import desc
from models.SmsModel import *
from models.SpamModel import *
from models.TrainningHistory import *
from datetime import datetime
import random

def clear_history_trainning():
    return engine.connect().execute('truncate trainning_history')

def trainning(db:Session):
    msg = list_all_sms(db)
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
    # clear_old_trainning()
    for word in vocabulary:
        add_word(db, word, int(number_word_occurs_spam_sms.get(word) or 0), int(number_word_occurs_normal_sms.get(word) or 0))
    add_trainning(db, words_spam/len(words), len(vocabulary), len(vocabulary_spam_sms), len(vocabulary_normal_sms))

def test_trainning(db:Session):
    max_range = count_sms(db)
    max_sms = 50
    if max_range < max_sms:
        max_sms = max_range
    start = random.randrange(0, max_range-max_sms-1)
    sms_list = list_sms(db, page=1, page_size=max_sms, start=start)
    split_text_to_word("123")
    correct = 0
    for sms in sms_list:
        label = is_sms_spam(db, sms.message_content)
        if label == True and sms.label == 2:
            correct = correct + 1
        if label == False and sms.label == 1:
            correct = correct + 1
    p_exactly = correct / max_sms
    last_trainning = get_last_trainning(db)
    last_trainning.p_exactly = p_exactly
    return save_trainning(db, last_trainning)
