# Dockerfile per il frontend (React)
# Usa l'immagine base di Node.js
FROM node:16-alpine

# Imposta la directory di lavoro
WORKDIR /app

# Copia il file package.json e package-lock.json nella directory di lavoro
COPY package*.json ./

# Installa le dipendenze
RUN npm install

# Copia il contenuto del frontend nell'immagine
COPY . .

# Compila l'app React per la produzione
RUN npm run build

# Installa un server statico per servire l'app React (ad esempio serve)
RUN npm install -g serve

# Esponi la porta su cui l'app sarà servita
EXPOSE 443

# Comando per eseguire l'app React
# CMD ["serve", "-s", "build",  "-l", "443"]
CMD [ "serve", "-s", "build", "-l", "443", "--ssl-cert", "nba-frontend.crt", "--ssl-key", "nba-frontend.key" ]
