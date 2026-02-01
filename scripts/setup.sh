#!/bin/bash
# Setup script for TapFlow development environment

set -e

echo "Setting up TapFlow development environment..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python $required_version or higher is required (found $python_version)"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements-dev.txt

# Create data directories
echo "Creating data directories..."
mkdir -p data/bronze data/silver data/gold

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
fi

if [ ! -f "docker/.env" ]; then
    echo "Creating docker/.env file from template..."
    cp docker/.env.example docker/.env
fi

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install

echo ""
echo "Setup complete!"
echo "To activate the virtual environment, run: source venv/bin/activate"
echo "To start services, run: make start"
