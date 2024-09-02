#!/bin/bash

export $(cat .env | xargs)

# Check if the container exists
if docker ps -a --format '{{.Names}}' | grep -q "^lexica-mongo$"; then
    
    # Check if the container is running
    if docker ps --format '{{.Names}}' | grep -q "^lexica-mongo$"; then
        echo "Container 'lexica-mongo' is running."
    else
        echo "Starting container 'lexica-mongo'..."
		docker start lexica-mongo
    fi
else
    echo "Creating container 'lexica-mongo'..."
    docker run -ditp ${MONGO_PORT}:${MONGO_PORT} --name lexica-mongo \
        -e MONGO_INITDB_ROOT_USERNAME=${MONGO_USERNAME} \
        -e MONGO_INITDB_ROOT_PASSWORD=${MONGO_PASSWORD} \
        mongo
fi
