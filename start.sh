#!/bin/bash

# Budowanie obrazu Docker
docker build -t application .

# Uruchamianie kontenera Docker i wystawianie portu 5000
docker run -p 5000:5000 -d application
