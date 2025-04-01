# Cahier des charges - Quantity Estimation

### Activité de l’application
Évaluation de traducteurs automatiques sans recours à une traduction de référence, en utilisant la méthode de **Quantity Estimation**. Pour cela, nous exploiterons des transformers de type BERT ainsi que des modèles génératifs comme Mistral. Enfin, l'évaluation sera réalisée à l'aide du module **TransQuest**. L'ensemble sera intégré dans une application web avec **FastAPI**.

### Objectifs
L'utilisateur dispose des fonctionnalitées suivantes :  
1. Choix de la langue source et de la langue cible  
2. Choix de la langue source et de la langue cible  
3. Afficher le résultat de la traduction dans la langue cible  
4. Afficher un score de fiabilité  
5. Interface claire, intéractive et jolie !

### Besoins
L’utilisateur devra :  
1. Sélectionner le modèle de traduction à utiliser  
2. Spécifier la langue du texte d’entrée (avec une possible amélioration future pour la détection automatique)  
3. Indiquer la langue cible pour la traduction  
4. Saisir le texte à traduire dans le champ approprié.

### Public
Des utilisateurs qui ne maîtrisent pas la langue cible et voudraient avoir un feedback sur la qualité de la traduction.

### État de l’art


## 1. Modèles de Traduction

### 1.1 MarianMT (Helsinki-NLP)

### 1.2 Mistral


## 2. Évaluation de la Traduction

### 2.1 Quantity Estimation (QE) : TransQuest
