from happytransformer import HappyTextToText, TTSettings
from collections import defaultdict
from curl_cffi import requests
from bs4 import BeautifulSoup as soup
import torch
from transquest.algo.sentence_level.siamesetransquest.run_model import SiameseTransQuestModel
import time

#__________FUNCTIONS

def translate(model, input_txt: str):
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