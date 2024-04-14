# Użyj oficjalny obraz oprogramowania Python jako bazowy obraz
FROM python:3.11-slim-buster

# Instalacja PHP
RUN apt-get update && apt-get install -y php

# Ustaw katalog roboczy na /app
WORKDIR /app

# Skopiuj plik requirements.txt do katalogu roboczego obrazu
COPY requirements.txt requirements.txt

# Zainstaluj zależności
RUN pip install -r requirements.txt

# Skopiuj pozostałe pliki do katalogu roboczego obrazu
COPY . .

# Uruchom aplikację przy użyciu komendy "python app.py"
CMD ["python", "app.py"]
