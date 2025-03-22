# Quantity Estimation

**Membres :** NGAUV Nicolas, SCHLOSSER Guilhem, THEZENAS Anissa

## Objectif

Crée une interface web pour permettre aux utilisateurs d'évaluer la fiabilité d'une traduction automatique.

### Scripts

Le dossier ***scripts*** rassemble deux fichiers python aussi qu'un fichier json.  
Installation des bibliothèques requise via : requirements.txt  
```pip install -r requirements.txt```

#### execution_steps.ipynb
Permet de suivre étape par étape les différentes phases de la traduction à l'évaluation.

#### main.py
Fichier utilisable en ligne de commande. Prend en entrée la langue source, la langue cible ainsi que le contenu textuel à traduire. Retourne deux fichiers dans le répertoire **Output**.

**Exemple: **  
```  
python3 main.py -src "French" -tgt "English (US)" -ipt "Bonsoir, quelle belle journée n'est ce pas ?"
```

### Output

