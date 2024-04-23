#!/bin/bash

export $(cat .env | xargs)

# Check if the container exists
if docker ps -a --format '{{.Names}}' | grep -q "^l2ai-mongo$"; then
    
    # Check if the container is running
    if docker ps --format '{{.Names}}' | grep -q "^l2ai-mongo$"; then
        echo "Container 'l2ai-mongo' is running."
    else
        echo "Starting container 'l2ai-mongo'..."
		docker start l2ai-mongo
    fi
else
    echo "Creating container 'l2ai-mongo'..."
    docker run -ditp ${MONGO_PORT}:${MONGO_PORT} --name l2ai-mongo \
        -e MONGO_INITDB_ROOT_USERNAME=${MONGO_USERNAME} \
        -e MONGO_INITDB_ROOT_PASSWORD=${MONGO_PASSWORD} \
        mongo
fi
