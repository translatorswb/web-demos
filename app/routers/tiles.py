from fastapi import Request, Form, APIRouter, File, UploadFile, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import json
from dotenv import load_dotenv
from typing import Optional
load_dotenv()

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

AUDIO_EXTS = ['.wav', '.WAV'] #Can be extended

garden = {"cherry tomato": "X7Hr9X4I1NY", "orchids": "LxkLc3arKHU", "roses": "OYbbldGNbr8", "mint": "Hw3HXrdt20o", "jalapeno": "i6NrodYFNhg",
          "idea":"LdxltzhYjHE", "ants":"62A2_gKuBaU"}

keywords = {"idea":["idea", "ideas", "start"], "ants":["ant", "ants"], "roses":["roses", "rose"], 
            "cherry tomato":["cherry", "tomato", "tomatoes"], "mint":["mint"], "jalapeno":["jalapeno", "pepper"]}

def say(text):
    url = "http://localhost:12101/api/text-to-speech"
    requests.post(url, text)

@router.get("/tilesrpi", response_class=HTMLResponse)
def get_vosk(request: Request, intent: Optional[str] = None):
    
    return templates.TemplateResponse('tilesrpi.html', context={'request': request})

@router.post("/tilesrpi/intent")
def get_vosk(intentstr: str = Form(...)):
    intentobj = json.loads(intentstr)
    intent = intentobj['intent']['name']
    slots = intentobj['slots']

    if intent == 'Grow' and slots['plant'] in garden:
        plant = slots['plant']
        print(intent, plant)

        say("Here's a video on how to grow" + plant)

        video_id = garden.get(plant)
        print('video_id', video_id)
        return {"found":True, "id": video_id}
    elif intent == 'Prevent':
        toprevent = slots['toprevent']
        print(intent, toprevent)

        say("Here's some tips on how to stop" + toprevent)

        video_id = garden.get(toprevent)
        print('video_id', video_id)
        return {"found":True, "id": video_id}
    elif intent == 'Stop':
        print("Stop")
        return {"found":False, "id":""}
    else:
        return {"found":False, "id":""}


# @router.post("/tilesrpi/command/")
# async def post_vosk(command: str = Form(...)):
#     print("Command:", command)

#     result = {"found":False, "id": ""}

#     if command in garden:
#         result = {"found":True, "id": garden[command]}
#     else:
#         for word in command.split():
#             for keyword in keywords:
#                 if word in keywords[keyword]:
#                     result = {"found":True, "id": garden[keyword]}

#     print(result)
    
#     return result

# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was: {data}")

