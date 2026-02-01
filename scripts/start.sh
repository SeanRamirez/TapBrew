#!/bin/bash
# Start TapFlow services

set -e

echo "Starting TapFlow services..."

cd docker
docker-compose up -d

echo "Waiting for services to be healthy..."
sleep 30

echo ""
echo "TapFlow is running!"
echo "================================"
echo "  API:      http://localhost:8000/docs"
echo "  Grafana:  http://localhost:3000 (admin/admin)"
echo "  Redpanda: http://localhost:8081"
echo ""
