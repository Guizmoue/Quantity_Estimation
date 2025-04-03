#__________MODULES
from happytransformer import HappyTextToText, TTSettings
from collections import defaultdict
from curl_cffi import requests
from bs4 import BeautifulSoup as soup
import torch
from transquest.algo.sentence_level.siamesetransquest.run_model import SiameseTransQuestModel
from utils import translate, score, save
import argparse
import json
import os
import time

#__________MODEL & DATA

os.environ["CUDA_VISIBLE_DEVICES"] = "-1" # Désactive l'utilisation du GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("PyTorch use :", device)  # Doit afficher "cpu"

print("\n----- LOADING MODEL -----")
start_m = time.perf_counter()
model_QE = SiameseTransQuestModel("TransQuest/siamesetransquest-da-multilingual")
model_QE.model.to(device)  # Transfert sur GPU si dispo
end_m = time.perf_counter()
timer_m = end_m - start_m
print(f"Model loaded : {timer_m:.6f} secondes")

# Chargement des tags de langue
with open("lang_tags.json", "r", encoding="utf-8") as f:
    lang_tags = json.load(f)

def main():
    """
    Programme principal : gère les arguments et exécute la traduction + scoring.
    """
    # Décrit le fonctionnement du programme
    parser = argparse.ArgumentParser(description="Traduction et l'évaluation de la traduction d'après la méthode de la Quantity Estimation (QE).")
    parser.add_argument("-src", "--source", type=str, required=True, help="Langue source")
    parser.add_argument("-tgt", "--target", type=str, required=True, help="Langue cible")
    parser.add_argument("-ipt", "--input", type=str, required=True, help="Texte à traduire")

    # Stocke les valeurs analysées dans l'objet my_args.
    args = parser.parse_args()

    # Initialiser les variables
    source = lang_tags[args.source]
    target = lang_tags[args.target]
    input_txt = args.input
    model_LANG = f"Helsinki-NLP/opus-mt-{source}-{target}"

    print("\n----- TRANSLATING -----")
    output_txt, timer_t = translate(model_LANG, input_txt)
    print(f"source : {input_txt}\ncible : {output_txt}")
    print(f"Translated in : {timer_t:.6f} secondes")
    save("./Output/translate.txt", output_txt)

    print("\n----- SCORING -----")
    score_QE = score(input_txt, output_txt)
    print(f"{float(score_QE)=}")
    save("./Output/score.txt", score_QE)


#__________MAIN
if __name__ == "__main__":
    main()

