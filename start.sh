#!/bin/bash

docker build -t application .

docker run --privileged -p 5000:5000 -d application

echo ""
echo "Citadela CTF setup completed!"
