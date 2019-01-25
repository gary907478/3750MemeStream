#!/bin/bash

set -e

echo "Stopping containers..."
docker kill server || true

echo "Deleting containers..."
docker rm server || true

sleep 1

echo "Starting server container..."
docker run -d -p 1269:8080 --net memestream --name server memeserver:latest
set +x

echo "To see logs of server, type 'docker logs -f server'"
echo "View website at http://localhost:1269"
