#__________MODULES
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Literal, Optional
from fastapi.middleware.cors import CORSMiddleware
import os
import json

from happytransformer import HappyTextToText, TTSettings
from collections import defaultdict
from curl_cffi import requests
from bs4 import BeautifulSoup as soup
import torch
from transquest.algo.sentence_level.siamesetransquest.run_model import SiameseTransQuestModel

from utils import LANG_DATABASE, MODEL_DATABASE, module_marian, module_google, module_deepl

#__________MODELS
app = FastAPI() # Création d'une instance FastAPI pour gérer l'application

# Configuration du moteur de templates Jinja2
templates = Jinja2Templates(directory="templates")

# Gestion des fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")

#__________LANGS
# Chargement des langues depuis un fichier JSON
LANG_DATABASE_FILE = "lang_tags.json"

if os.path.exists(LANG_DATABASE_FILE):
    with open(LANG_DATABASE_FILE, "r", encoding="utf8") as f:
        LANG_DATABASE = json.load(f)

#__________INDEX

# Dans la page d'acceuil index.html instancier la variable "langues" qui correspond au contenu du fichier lang_tags.json
@app.get("/")
async def root(request: Request):
    context = {"request": request,  "models": MODEL_DATABASE, "languages": LANG_DATABASE}
    return templates.TemplateResponse("index.html", context)

# Dans la page d'acceuil index.html récupérer les valeurs du formulaire faire la traduction et renvoyer le texte et le score dans la page
@app.post("/submit/", response_class=HTMLResponse)
async def get_parameters(
    request: Request, 
    model: str = Form(...), 
    lang_src: str = Form(...),
    lang_tgt: str = Form(...),
    text_src: str = Form(...)
    ):

    print(f"{model=}")
    print(f"{lang_src=}, {lang_tgt=}")
    print(f"{text_src=}")

    if model == "Deepl":
        text_tgt, score_QE = module_deepl(model, lang_src, lang_tgt, text_src)
    elif model == "Google Translate":
        text_tgt, score_QE = module_google(model, lang_src, lang_tgt, text_src)
    elif model == "Marian-NMT":
        text_tgt, score_QE = module_marian(model, lang_src, lang_tgt, text_src)

    context = {"request": request, "models": MODEL_DATABASE, "model_selected": model, "languages": LANG_DATABASE, "lang_src": lang_src, "lang_tgt": lang_tgt, "text_src": text_src, "text_tgt": text_tgt, "score": int(score_QE)}
    return templates.TemplateResponse("index.html", context)
