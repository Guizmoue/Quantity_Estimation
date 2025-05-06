# Image de Python
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app
#COPY requirements.txt .
#RUN pip install --upgrade pip && pip install -r requirements.txt

# Copier les fichiers de l'application dans le conteneur
COPY . /app

# Installer les éventuels paquets systèmes nécessaires à l'application
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

# Installer les dépendances
RUN pip install -r requirements.txt

# Exposer le port sur lequel l'application va tourner
EXPOSE 8005

# Commande pour lancer l'application FastAPI avec Uvicorn
CMD ["uvicorn", "web:app", "--host", "0.0.0.0", "--port", "8000"]

