FROM python:3.11-slim-buster # do not change

RUN apt-get update && apt-get install -y php util-linux && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
