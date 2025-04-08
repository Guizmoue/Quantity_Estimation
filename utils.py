from happytransformer import HappyTextToText, TTSettings
from transquest.algo.sentence_level.siamesetransquest.run_model import SiameseTransQuestModel
from deep_translator import GoogleTranslator
import deepl

import torch
import time
import json
import config
import os

#__________LANGUAGE_MODEL
os.environ["CUDA_VISIBLE_DEVICES"] = "-1" # Désactive l'utilisation du GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_QE = SiameseTransQuestModel("TransQuest/siamesetransquest-da-multilingual")
model_QE.model.to(device)  # Transfert sur GPU si disponible

#__________MODELS
MODEL_DATABASE = {
    "Deepl": "deepl",
    "Google Translate": "google-translate",
    "Marian-NMT": "Helsinki-NLP/opus-mt"
}

#__________LANGS
# Chargement des langues depuis un fichier JSON
LANG_DATABASE_FILE = "lang_tags.json"

if os.path.exists(LANG_DATABASE_FILE):
    with open(LANG_DATABASE_FILE, "r", encoding="utf8") as f:
        LANG_DATABASE = json.load(f)

#__________FUNCTIONS

def marian_translate(model, input_txt: str):
    """
    Traduit un texte donné en utilisant HappyTextToText.
    """
    start_t = time.perf_counter()
    settings = TTSettings(do_sample=True, top_k=50, temperature=0.7)
    happy_tt = HappyTextToText("MARIAN", model)
    output_txt = happy_tt.generate_text(input_txt, args=settings).text
    end_t = time.perf_counter()
    timer_t = end_t - start_t
    
    return output_txt, timer_t

def score(model_QE, input_txt: str, output_txt: str):
    """
    Évalue la qualité de la traduction en prédisant un score de Quantity Estimation.
    """
    return model_QE.predict([[input_txt, output_txt]])

def save(path, content):
    """
    Sauvegarde un contenu textuel dans un fichier.
    """
    with open(path, "w", encoding="utf8") as file:
        file.write(str(content))


def module_deepl(model: str, lang_src: str, lang_tgt: str, text_src: str):
    print(f"{model=}")
    
    auth_key = config.api_key
    translator = deepl.Translator(auth_key)
    outputs = translator.translate_text(text_src, source_lang=LANG_DATABASE[lang_src].upper(), target_lang=LANG_DATABASE[lang_tgt].upper())
    text_tgt = outputs.text
    print(f"{text_tgt=}")

    score_QE = score(model_QE, text_src, text_tgt)
    score_QE = int(round(float(score_QE), 2) * 100)
    print(f"{score_QE=}")

    return text_tgt, score_QE


def module_google(model: str, lang_src: str, lang_tgt: str, text_src: str):
    print(f"{model=}")
    
    text_tgt = GoogleTranslator(source=LANG_DATABASE[lang_src], target=LANG_DATABASE[lang_tgt]).translate(text=text_src)
    print(f"{text_tgt=}")

    score_QE = score(model_QE, text_src, text_tgt)
    score_QE = int(round(float(score_QE), 2) * 100)
    print(f"{score_QE=}")

    return text_tgt, score_QE


def module_marian(model: str, lang_src: str, lang_tgt: str, text_src: str):
    model = f"{MODEL_DATABASE[model]}-{LANG_DATABASE[lang_src]}-{LANG_DATABASE[lang_tgt]}"
    print(f"{model=}")

    text_tgt, timer_t = marian_translate(model, text_src)
    print(f"{text_tgt=}")

    score_QE = score(model_QE, text_src, text_tgt)
    score_QE = int(round(float(score_QE), 2) * 100)
    print(f"{score_QE=}")

    return text_tgt, score_QE