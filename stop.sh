#!/bin/bash

set -e

echo "Stopping containers..."

docker kill db server || true

echo "Deleting containers..."
docker rm db server || true

echo "Deleting network..."
docker network prune -f

echo "done"
