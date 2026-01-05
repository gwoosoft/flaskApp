#!/bin/bash

# Build images (in case you made changes to your app)
docker-compose build

# Start all containers in detached mode, remove old/unused containers, and recreate if needed
docker-compose up -d --remove-orphans --force-recreate

echo "Flask app is running on http://localhost"
