#!/bin/bash
# Stop TapFlow services

set -e

echo "Stopping TapFlow services..."

cd docker
docker-compose down

echo "All services stopped."
