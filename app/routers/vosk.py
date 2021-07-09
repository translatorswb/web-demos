from fastapi import Request, Form, APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..library.helpers import *
#import httpx
import requests
import json
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

AUDIO_EXTS = ['.wav', '.WAV'] #Can be extended

garden = {"cherry tomato": "X7Hr9X4I1NY", "orchids": "LxkLc3arKHU", "roses": "OYbbldGNbr8", "mint": "Hw3HXrdt20o", "jalapeno": "i6NrodYFNhg",
          "idea":"LdxltzhYjHE", "ants":"62A2_gKuBaU"}

keywords = {"idea":["idea", "ideas", "start"], "ants":["ant", "ants"], "roses":["roses", "rose"], 
            "cherry tomato":["cherry", "tomato", "tomatoes"], "mint":["mint"], "jalapeno":["jalapeno", "pepper"]}


@router.get("/vosk", response_class=HTMLResponse)
def get_vosk(request: Request):
    result = "This app is not working yet"
    
    return templates.TemplateResponse('vosk.html', context={'request': request, 'text': result})


@router.post("/vosk/command/")
async def post_vosk(command: str = Form(...)):
    print("Command:", command)

    result = {"found":False, "id": ""}

    if command in garden:
        result = {"found":True, "id": garden[command]}
    else:
        for word in command.split():
            for keyword in keywords:
                if word in keywords[keyword]:
                    result = {"found":True, "id": garden[keyword]}

    print(result)
    
    return result
