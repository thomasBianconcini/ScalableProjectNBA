# Dockerfile per il backend (Flask)
# Usa l'immagine base di Python
FROM python:3.9-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia il file requirements.txt nella directory di lavoro
COPY requirements.txt .

# Installa le dipendenze Python
RUN pip install -r requirements.txt

# Copia il contenuto del backend nell'immagine
COPY . .

# Esponi la porta su cui l'app Flask sarà in ascolto
EXPOSE 5000

# Comando per eseguire l'app Flask
CMD ["python", "app.py"]
