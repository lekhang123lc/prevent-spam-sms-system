# localhost:8000
# uvicorn main:app --reload
from fastapi import FastAPI
from model import *
from db import engine
from db import SessionLocal
from fastapi import Depends
import pandas as pd
from collections import OrderedDict

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/")
async def index():
    print("get")
    return {"message": "GET Hello World"}

@app.post("/")
async def detectSpam(message: Message, db:Session = Depends(get_db)):
    msg = message.phone_number_send + " " + message.phone_number_receive + " " + str(message.message_status) + " " + message.message_subject+ " " + message.message_content + " " + message.message_date
    #add_sms(db, message)
    print(msg)
    # true if this msg is spam, false if not
    return {"result": isSpam(db, message.message_content )}

@app.get("/init")
async def init(db:Session = Depends(get_db)):
    sms_spam = pd.read_csv('data/SMSSpamCollection', sep='\t', header=None, names=['Label', 'SMS'])
    clear_all_sms()
    #for i in range(len(sms_spam['Label'])):
    for i in range(100):
        msg_label = 2
        if sms_spam['Label'][i] == "ham": msg_label=1
        msg = Message(
            phone_number_send="000000000",
            phone_number_receive="000000000",
            message_status=1,
            message_subject="EMPTY_SUBJECT",
            message_content=sms_spam['SMS'][i],
            message_date="00:00:00 00/00/0000"
        )
        add_sms(db, msg, label=msg_label)
    return {"message": "OK init table sms"}

@app.get("/list")
async def getList(db:Session = Depends(get_db)):
    msg = list_sms(db)
    return {"message": msg}

@app.get("/train")
async def train(db:Session = Depends(get_db)):
    trainning(db)
    return {"message": "ok"}

@app.get("/{id}")
async def getMessage(id: int, db:Session = Depends(get_db)):
    msg = get_sms(db, id)
    return {"message": msg}

