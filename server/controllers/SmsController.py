from ast import Continue
from email import message
from fastapi import FastAPI
from fastapi import APIRouter
from database.db import *
from fastapi import Request
from fastapi.responses import HTMLResponse
from models.SmsModel import *
from models.SpamModel import *
from fastapi.responses import RedirectResponse
import dateutil.parser as parser
from fastapi import FastAPI, File, UploadFile

router = APIRouter(
    prefix="/sms",
    tags=["SMS"],
    responses={404: {"description": "Not found"}},
)

database = Database()
engine = database.get_db_connection()

@router.post("/classifier")
async def detectSpam(message: Message, test=0):
    db = database.get_db_session(engine)
    msg = message.phone_number_send + " " + message.phone_number_receive + " " + str(message.message_status) + " " + message.message_subject+ " " + message.message_content + " " + message.message_date
    if test == 0:
        add_sms(db, message)
    # print(msg)
    # true if this msg is spam, false if not
    if is_sms_spam(db, message.message_content):
        return {"result": "spam"}
    else :
        return {"result": "ham"}

@router.get("/list", response_class=HTMLResponse)
async def getListMessage(request : Request, page=1):
    db = database.get_db_session(engine)
    page = int(page)
    messages = list_sms(db, page)
    pages = []
    start = page-2
    max_page = get_max_page(db)
    while start <= page+2:
        if start > 0 and start <= max_page:
            pages.append(start)
        start=start+1
    return templates.TemplateResponse("sms/list.html", { "request": request, "messages": messages, "current_page": page, "max_page": max_page, "pages": pages})

@router.get("/add")
async def createMessage(request : Request):
    return templates.TemplateResponse("sms/add.html", { "request": request})

@router.get("/edit/{id}")
async def editMessage(request : Request, id:int):
    db = database.get_db_session(engine)
    sms = get_sms(db, id)
    print(sms.message_date)
    msg_date = parser.parse(sms.message_date)
    return templates.TemplateResponse("sms/edit.html", { "request": request, "sms": sms, "msg_date": msg_date})

@router.post("/save/{id}")
async def saveMessage(sms: SMS_Server, id:int):
    db = database.get_db_session(engine)
    if id == 0:
        msg = Message(
            phone_number_send=sms.phone_number_send,
            phone_number_receive=sms.phone_number_receive, 
            message_status=sms.message_status, 
            message_subject=sms.message_subject, 
            message_content=sms.message_content, 
            message_date=sms.message_date 
        )
        add_sms(db, msg, label=sms.label)
    else:
        msg = SMS(
            id=id,
            phone_number_send=sms.phone_number_send,
            phone_number_receive=sms.phone_number_receive, 
            message_status=sms.message_status, 
            message_subject=sms.message_subject, 
            message_content=sms.message_content, 
            message_date=sms.message_date,
            label=sms.label
        )
        update_sms(db, msg)
    # return RedirectResponse("/sms/list")
    return {"msg": "ok"}

@router.post("/delete/{id}")
async def deleteMessage(id: int):
    db = database.get_db_session(engine)
    msg = get_sms(db, id)
    return {"message": msg}

@router.post("/add-list")
async def addList(file: UploadFile):
    db = database.get_db_session(engine)
    add_list(db, file)
    return ""
