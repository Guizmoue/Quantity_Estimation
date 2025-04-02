from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from happytransformer import HappyTextToText, TTSettings
import json
import torch
import os
import time
from transquest.algo.sentence_level.siamesetransquest.run_model import SiameseTransQuestModel

# Initialisation de l'application FastAPI
app = FastAPI()

# Configuration des fichiers statiques (JS, CSS) et des templates (HTML)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Chargement des tags de langue
with open("lang_tags.json", "r", encoding="utf-8") as f:
    lang_tags = json.load(f)

# Désactiver l'utilisation du GPU (optionnel, dépend du matériel)
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Chargement du modèle de Quality Estimation (QE)
print("\n----- LOADING MODEL -----")
start_m = time.perf_counter()
model_QE = SiameseTransQuestModel("TransQuest/siamesetransquest-da-multilingual")
model_QE.model.to(device)  # Transfert sur GPU si dispo
end_m = time.perf_counter()
print(f"Model loaded in {end_m - start_m:.2f} seconds")


# Fonction de traduction
def translate(model, input_txt: str):
    """
    Traduit un texte donné en utilisant HappyTextToText.
    """
    start_t = time.perf_counter()
    settings = TTSettings(do_sample=True, top_k=50, temperature=0)
    happy_tt = HappyTextToText("MARIAN", model)
    output_txt = happy_tt.generate_text(input_txt, args=settings).text
    end_t = time.perf_counter()

    return output_txt, end_t - start_t


# Fonction d'évaluation de qualité de traduction
def score(input_txt: str, output_txt: str):
    """
    Évalue la qualité de la traduction avec le modèle SiameseTransQuest.
    """
    #return model_QE.predict([[input_txt, output_txt]])[0]  # On récupère le score
    return float(model_QE.predict([[input_txt, output_txt]]))


# Page principale (renvoie l'interface utilisateur)
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Modèle de données pour la requête de traduction
class TranslationRequest(BaseModel):
    source: str
    target: str
    text: str


# Endpoint de traduction
@app.post("/translate")
async def translate_text(req: TranslationRequest):
    """
    Endpoint qui reçoit du texte, effectue la traduction et évalue sa qualité.
    """
    source = req.source
    target = req.target
    input_txt = req.text

    # Vérification que la langue est prise en charge
    if source not in lang_tags.values() or target not in lang_tags.values():
        return {"error": "Langue non prise en charge."}

    # Sélection du modèle Helsinki-NLP adapté aux langues choisies
    model_LANG = f"Helsinki-NLP/opus-mt-{source}-{target}"

    # Traduction du texte
    output_txt, _ = translate(model_LANG, input_txt)

    # Calcul du score de qualité de la traduction
    score_QE = score(input_txt, output_txt)

    return {"translation": output_txt, "score": score_QE}
