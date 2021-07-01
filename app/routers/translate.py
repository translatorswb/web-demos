from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
import httpx
import json
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()

templates = Jinja2Templates(directory="templates/")

MT_API_URL = os.getenv("MT_API_URL")
#   GAMAYUN_API_TOKEN = os.getenv("API_TOKEN")
MAX_REQUEST_LENGTH = int(os.getenv('MAX_REQUEST_LENGTH') or "5000")


INIT_MESSAGE = ""
INIT_SRC = "fr"
INIT_TGT = "en"

def get_language_info():
    translate_url = MT_API_URL
    api_languages = {}
    api_models = {}

    if translate_url:
        try:
            r = httpx.get(translate_url)
        except httpx.HTTPError as exc:
            print(f"Error while requesting {exc.request.url!r}.")
            print(exc)
            return api_languages, api_models

        if r.status_code == 200:
            response = r.json()

            api_languages = response['languages']
            api_models = response['models']
     
        else:
            print("Error retrieving language list")
            try:
                print(response['detail'])
            except:
                print("No response from MT server")

    return api_languages, api_models


@router.get("/translate")
def form_get(request: Request):
    api_languages, api_models = get_language_info()

    if INIT_SRC and INIT_SRC in api_models and INIT_TGT and INIT_TGT in api_models[INIT_SRC]:
        src_select = INIT_SRC
        tgt_select = INIT_TGT
    elif len(api_models) >= 1:
        #select first model
        src_select = list(api_models)[0] 
        tgt_select = list(api_models[src_select])[0]
    else:
        src_select = ''
        tgt_select = ''

    #print("Select: %s-%s"%(src_select,tgt_select))

    return templates.TemplateResponse('translate.html', context={'request': request, 'api_languages':api_languages, 'api_models':api_models, 'src':src_select, 'tgt':tgt_select, 'source': INIT_MESSAGE, 'text1': '', 'text2': '', 'maxlength':MAX_REQUEST_LENGTH})


@router.post("/translate")
async def form_post(request: Request):
    form = await request.form()
    message = form['message']
    src = form['src']
    tgt = form['tgt']
    disclaimer = ''

    api_languages, api_models = get_language_info()

    if len(message) > MAX_REQUEST_LENGTH:
        result = 'Requests must contain %i characters or less.'%MAX_REQUEST_LENGTH
    elif message and src in api_models and tgt in api_models[src]:
        translate_service_url = MT_API_URL
        
        json_data = {'src':src, 
                     'tgt':tgt,
                     'text':message}
                     # 'token':GAMAYUN_API_TOKEN}

        try:
            r = httpx.post(translate_service_url, json=json_data)

            if r.status_code == 200:
                usage_load = len(message.split())
                model_info = {'src':src, 'tgt':tgt}

                response = r.json()
                result = response['translation']
                disclaimer = response['disclaimer'] if 'disclaimer' in response else disclaimer
            else:
                result = r.json()['detail']
        except httpx.HTTPError as exc:
            print(f"Error while requesting {exc.request.url!r}.")
            print(exc)
            result = 'Translate service not available.'
    else:
        result = ''

    
    return templates.TemplateResponse('translate.html', context={'request': request, 'api_languages':api_languages, 'api_models':api_models, 'src':src, 'tgt':tgt, 'source': message, 'text1': result, 'text2': '', 'disclaimer':disclaimer, 'maxlength':MAX_REQUEST_LENGTH})
