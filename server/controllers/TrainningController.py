from ast import Continue
from fastapi import FastAPI
from fastapi import APIRouter
from database.db import *
from fastapi import Request
from fastapi.responses import HTMLResponse
from models.SmsModel import *
from models.SpamModel import *
from models.TrainningModel import *
from fastapi.responses import RedirectResponse
import dateutil.parser as parser

router = APIRouter(
    prefix="/trainning",
    tags=["SMS"],
    responses={404: {"description": "Not found"}},
)

database = Database()
engine = database.get_db_connection()

@router.get("/list", response_class=HTMLResponse)
async def getListTrainning(request : Request, page=1):
    db = database.get_db_session(engine)
    page = int(page)
    trainning_history = list_trainning(db, page)
    pages = []
    start = page-2
    max_page = get_max_page_trainning(db)
    while start <= page+2:
        if start > 0 and start <= max_page:
            pages.append(start)
        start=start+1
    return templates.TemplateResponse("trainning/list.html", { "request": request, "trainning_history": trainning_history, "current_page": page, "max_page": max_page, "pages": pages})

@router.get("/train", response_class=HTMLResponse)
async def train(request : Request):
    db = database.get_db_session(engine)
    trainning(db)
    
    page = int(1)
    trainning_history = list_trainning(db, page)
    pages = []
    start = page-2
    max_page = get_max_page_trainning(db)
    while start <= page+2:
        if start > 0 and start <= max_page:
            pages.append(start)
        start=start+1
    return templates.TemplateResponse("trainning/list.html", { "request": request, "trainning_history": trainning_history, "current_page": page, "max_page": max_page, "pages": pages})

@router.get("/test", response_class=HTMLResponse)
async def test(request : Request):
    db = database.get_db_session(engine)
    test_trainning(db)
    page = int(1)
    trainning_history = list_trainning(db, page)
    pages = []
    start = page-2
    max_page = get_max_page_trainning(db)
    while start <= page+2:
        if start > 0 and start <= max_page:
            pages.append(start)
        start=start+1
    return templates.TemplateResponse("trainning/list.html", { "request": request, "trainning_history": trainning_history, "current_page": page, "max_page": max_page, "pages": pages})