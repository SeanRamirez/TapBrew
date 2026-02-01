.PHONY: help setup start stop restart logs test coverage clean deploy

help:
	@echo "TapFlow - Available Commands"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  make setup         - Initial project setup"
	@echo "  make start         - Start all services"
	@echo "  make stop          - Stop all services"
	@echo "  make restart       - Restart all services"
	@echo "  make logs          - View logs (ctrl+c to exit)"
	@echo "  make test          - Run all tests"
	@echo "  make coverage      - Run tests with coverage"
	@echo "  make clean         - Clean up containers and data"
	@echo "  make generate-data - Generate synthetic data"
	@echo "  make deploy        - Deploy to cloud"

setup:
	@echo "Setting up TapFlow..."
	cp docker/.env.example docker/.env
	mkdir -p data/bronze data/silver data/gold
	pip install -r requirements-dev.txt
	pre-commit install
	@echo "Setup complete! Run 'make start' to begin."

start:
	@echo "Starting TapFlow services..."
	cd docker && docker-compose up -d
	@echo "Waiting for services to be healthy..."
	sleep 30
	@echo ""
	@echo "TapFlow is running!"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  API:      http://localhost:8000/docs"
	@echo "  Airflow:  http://localhost:8080 (admin/admin)"
	@echo "  Grafana:  http://localhost:3000 (admin/admin)"
	@echo "  Redpanda: http://localhost:8081"
	@echo ""

stop:
	@echo "Stopping TapFlow services..."
	cd docker && docker-compose down

restart: stop start

logs:
	cd docker && docker-compose logs -f

test:
	pytest tests/ -v --tb=short

coverage:
	pytest tests/ --cov=src --cov-report=html --cov-report=term
	@echo "Coverage report: htmlcov/index.html"

clean:
	@echo "Cleaning up..."
	cd docker && docker-compose down -v
	rm -rf data/bronze/* data/silver/* data/gold/*
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Cleanup complete"

generate-data:
	@echo "Generating synthetic data..."
	python src/data_generator/main.py --breweries 50 --days 30

deploy:
	@echo "Deploying TapFlow..."
	./scripts/deploy.sh
