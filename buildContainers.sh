#!/bin/bash

set -e 
set -x

echo "Building..."

docker build -t memedb:latest db/

docker build -t memeserver:latest server/

echo "done"
