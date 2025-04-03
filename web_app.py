#__________MODULES
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Literal, Optional
# from uuid import uuid4
# from fastapi.encoders import jsonable_encoder
import os
import json

from happytransformer import HappyTextToText, TTSettings
from collections import defaultdict
from curl_cffi import requests
from bs4 import BeautifulSoup as soup
import torch
from transquest.algo.sentence_level.siamesetransquest.run_model import SiameseTransQuestModel

from utils import translate, score

#__________MODELS
MODEL_DATABASE = {
    "Marian-NMT": "Helsinki-NLP/opus-mt"
}

os.environ["CUDA_VISIBLE_DEVICES"] = "-1" # Désactive l'utilisation du GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_QE = SiameseTransQuestModel("TransQuest/siamesetransquest-da-multilingual")
model_QE.model.to(device)  # Transfert sur GPU si dispo

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

# print(LANG_DATABASE)


#__________INDEX

# Dans la page d'acceuil index.html instancier la variable "langues" qui correspond au contenu du fichier lang_tags.json
@app.get("/")
async def root(request: Request):
    context = {"request": request, "langues": LANG_DATABASE}
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

    model = f"{MODEL_DATABASE[model]}-{LANG_DATABASE[lang_src]}-{LANG_DATABASE[lang_tgt]}"
    print(f"{model=}")
    print(f"{text_src=}")

    text_tgt, timer_t = translate(model, text_src)
    print(f"{text_tgt=}")
    
    score_QE = score(model_QE, text_src, text_tgt)
    score_QE = int(round(float(score_QE), 2) * 100)
    print(f"{score_QE=}")

    context = {"request": request, "langues": LANG_DATABASE, "text_tgt": text_tgt, "score": int(score_QE)}
    return templates.TemplateResponse("index.html", context)



#__________FORM
# # Définition du modèle de traduction
# class TranslationParameters(BaseModel):
#     model: str
#     lang_src: str
#     lang_tgt: str
#     text_src: str

# @app.post("/")
# def form_post(request: Request, parameters: TranslationParameters):
#     result = spell_number(num)
#     return templates.TemplateResponse('index.html', context={'request': request, 'result': result})



# @app.post("/", response_class=HTMLResponse)
# async def get_parameters(
#     request: Request,
#     model: str = Form(...),
#     lang_src: str = Form(...),
#     lang_tgt: str = Form(...),
#     text_src: str = Form(...)
# ):
#     # Vérification des valeurs
#     if not model or not lang_src or not lang_tgt or not text_src:
#         return JSONResponse(content={"error": "Tous les champs sont obligatoires"}, status_code=400)


# # Définition du modèle de traduction
# class TranslationParameters(BaseModel):
#     model: str
#     lang_src: str
#     lang_tgt: str
#     text_src: str

# @app.post("/", response_class=HTMLResponse)
# async def get_parameters(request: Request):
#     # Récupération des valeurs du formulaire
#     form_data = await request.form()
#     parm_model = form_data.get('model')
#     parm_lang_src = form_data.get('lang_src')  
#     parm_lang_tgt = form_data.get('lang_tgt')  
#     parm_text_src = form_data.get('text_src')    

#     # Création de l'objet TranslationParameters
#     parameters = TranslationParameters(
#         model=parm_model,
#         lang_src=parm_lang_src,
#         lang_tgt=parm_lang_tgt,
#         text_src=parm_text_src
#     )

#     print(parameters.dict())  # Debug dans la console

#     return templates.TemplateResponse(
#             "index.html", 
#             {
#                 "request": request,
#                 "langues": LANG_DATABASE,
#                 "result": parameters.dict()
#             }
#         )


#__________INDEX


# #___INTRO
# # Définition de la route GET sur "/" (racine du site)
# @app.get("/")
# async def root():
#     return {"message": "Hello World"} # renvoie un message "Hello World"

# # Définition de la route POST sur "/"
# @app.post("/") 
# async def post():
#     return {"message": "the post route"} # requêtes POST et renvoie un message spécifique

# # Définition de la route PUT sur "/"
# @app.put("/")
# async def put():
#     return {"message": "the put route"} # requêtes PUT et renvoie un message spécifique

# # Définition d'une route GET pour "/users"
# @app.get("/users") 
# async def list_users():
#     return {"message": "list users route"} # message indiquant que la liste des utilisateurs est accessible

# # Définition d'une route GET dynamique pour récupérer un utilisateur spécifique via son ID
# @app.get("/users/{user_id}")
# async def get_items(user_id: str):
#     return {"user_id": user_id} # L'ID de l'utilisateur est récupéré dans l'URL et renvoyé dans la réponse


# #___PATH PARAMS
# # Définition d'une énumération FoodEnum qui représente trois types d'aliments
# class FoodEnum(str, Enum):
#     fruits = "fruits"
#     vegies = "vegies"
#     dairy = "dairy"

# @app.get("/foods/{food_name}")
# async def get_food(food_name: FoodEnum):
#     """
#     Cette fonction prend un paramètre `food_name` (qui doit appartenir à FoodEnum)
#     et retourne un message différent selon la catégorie de nourriture choisie.
#     """
#     if food_name.value == "fruits":
#         return {"food_name": food_name, "message": "so sweet"}
#     elif food_name.value == "vegies":
#         return {"food_name": food_name, "message": "so healthy"}
#     else:
#         return {"food_name": food_name, "message": "so good"}

# #___QUERY PARAMS
# # Base de données fictive sous forme de liste de dictionnaires
# fake_item_db = [{"item_name": "Foo"}, {"item_name": "Baz"}, {"item_name": "Bar"}]

# @app.get("/items")
# async def list_items(skip: int):
#     """
#     Cette fonction retourne un élément de la base de données en fonction de l'index `skip`.
#     """
#     return fake_item_db[skip] # Retourne l'élément situé à l'index `skip`

# # Route GET pour récupérer un élément spécifique et l'utilisateur associé
# @app.get("/items/{item_id}/users/{user_id}")
# async def get_item(item_id: str, user_id: int, query: str | None = None, short: bool = False):
#     """
#     Cette fonction récupère un élément donné (`item_id`) associé à un utilisateur (`user_id`).
#     - `query` est un paramètre facultatif qui ajoute une information supplémentaire.
#     - `short` est un paramètre booléen qui conditionne l'ajout d'une description.
#     """
#     item = {"item_id": item_id, "user_id": user_id}
#     if query:
#         item.update({"query": query})
#     if not short:
#         item.update({"description": "en couple"})
#     return item # Retourne l'objet mis à jour


# #___REQUEST BODY
# # Définition du modèle de données pour un item
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float

# @app.post("/price")
# async def create_item(item: Item):
#     """
#     Cette fonction prend un objet `Item`, 
#     calcule le prix total avec taxes,
#     et renvoie un dictionnaire mis à jour.
#     """
#     item_dict = item.dict()
#     if item.price and item.tax:
#         new_price = item.price + item.tax*item.price
#         item_dict.update({"new price": new_price})
#     return item_dict

#___LINK HTML
# @app.get("/") # root page : index
# def index(req: Request):
#     return template.TemplateResponse(
#         name="index.html",
#         context={"request": req}
#         )

# if __name__ == "__main__":
#     uvicorn.run("main:app --reload")
#___LINK HTML