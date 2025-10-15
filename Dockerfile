# Utiliser une image officielle Python

FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system deps required for some Python packages (kept minimal).
RUN apt-get update && \
	apt-get install -y --no-install-recommends gcc libpq-dev build-essential curl && \
	rm -rf /var/lib/apt/lists/*

# Copier les fichiers du projet
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port de FastAPI
EXPOSE 8000

# Commande de lancement du serveur FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers du projet
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port de FastAPI
EXPOSE 8000

# Commande de lancement du serveur FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
