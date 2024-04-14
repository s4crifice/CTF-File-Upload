#!/bin/bash

## sometimes it's getting stuck on downloading packages
## in this case just CTRL + C and try again

docker build -t application .

docker run --privileged -p 5000:5000 -d application

echo ""
echo "Citadela CTF setup completed!"
