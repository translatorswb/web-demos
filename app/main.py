from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .library.helpers import *
from app.routers import transcribe, translate, vosk
from dotenv import load_dotenv
load_dotenv()

import mimetypes
mimetypes.init() 

app = FastAPI()


templates = Jinja2Templates(directory="templates")

mimetypes.add_type('application/javascript', '.js')
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(transcribe.router)
app.include_router(translate.router)
app.include_router(vosk.router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("home.md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})


@app.get("/page/{page_name}", response_class=HTMLResponse)
async def show_page(request: Request, page_name: str):
    data = openfile(page_name+".md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})
