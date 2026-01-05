#!/bin/bash

# Build images first (if you made changes to app)
docker-compose build

# Start all containers in detached mode
docker-compose up -d

echo "Flask app is running on http://localhost"
