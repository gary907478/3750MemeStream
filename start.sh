#!/bin/bash

set -e

./stop.sh 

echo "Pruning old docker network..."
docker network prune -f

echo "Creating docker network..."
docker network create memestream

echo "Starting db container..."
docker run -d -p 3306:3306 --net memestream --name db memedb:latest --default-authentication-plugin=mysql_native_password

echo "Starting server container..."
docker run -d -p 1269:8080 --net memestream --name server memeserver:latest
set +x

echo "To see logs of db, type 'docker logs -f db'"
echo "To see logs of server, type 'docker logs -f server'"
echo "View website at http://localhost:1269"

