#!/bin/bash

docker build -t application .
docker run -p 5000:5000 -d application
service apache2 restart


