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

ASR_API_URL = os.getenv("ASR_API_URL")
AUDIO_EXTS = ['.wav', '.WAV', '.mp3', '.MP3', '.m4a', '.M4A'] #Can be extended
INIT_LANG = 'swc'

def get_language_info():
    transcribe_url = ASR_API_URL
    api_languages = {}

    try:
        r = requests.request("GET", transcribe_url)
    except Exception as exc:
        print("Error while requesting language list from %s"%transcribe_url)
        print(exc)
        return api_languages

    if r.status_code == 200:
        response = r.json()
        api_languages = response['languages']
    else:
        print("Error retrieving language list")

    return api_languages

@router.get("/transcribe", response_class=HTMLResponse)
def get_upload(request: Request):
    api_langs =  get_language_info()

    if not api_langs:
        result = "Transcribe service not available"
    else:
        result = "Select or record an audio file to transcribe"

    print(api_langs)

    return templates.TemplateResponse('transcribe.html', context={'request': request, 'text': result, 'api_languages':api_langs, 'lang':INIT_LANG})


@router.post("/transcribe/new/")
async def post_upload(file: UploadFile = File(...), lang: str = Form(...), scorer: str = Form(...)): 
    print('Request in %s'%lang)
    print("With scorer", scorer)

    # create the directory path
    workspace = create_workspace()
    # filename
    file_name = Path(file.filename)
    print(file.filename)
    print(type(file.filename))
    # image full path
    img_full_path = workspace / file_name
    print(img_full_path)

    #TODO: Check file extension
    if not os.path.splitext(file.filename)[1] in AUDIO_EXTS:
        print("File not audio")
        return {'text':'ERROR: Please upload an audio with extension %s'%AUDIO_EXTS}

    with open(str(img_full_path), 'wb') as myfile:
        contents = await file.read()
        myfile.write(contents)

    
    #Send to ASR API
    transcribe_url = ASR_API_URL + 'short'
    print(transcribe_url)
    
    if scorer:
        payload={'lang': lang, 'scorer':scorer}
    else:
        payload={'lang': lang}

    files=[('file',(file.filename, open(img_full_path,'rb'), 'audio/wav'))]
    headers = {}
    print(files)

    try:
        response = requests.request("POST", transcribe_url, headers=headers, data=payload, files=files)
    except:
        result = "Transcribe service not available"
        
    if response.status_code == 200:
        response_json = response.json()
        result = response_json['transcript']
    else:
        response_json = response.json()
        result = "ERROR: " + response_json['detail']


    #Cleanup
    os.remove(img_full_path)
    os.rmdir(workspace)

    return {"text": result}
