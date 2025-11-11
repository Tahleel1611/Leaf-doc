#!/bin/bash
# Quick start script for LeafDoc API

echo "========================================"
echo "LeafDoc API - Quick Start"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Check if requirements are installed
python -c "import fastapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Create directories
echo "Creating storage directories..."
mkdir -p storage/images storage/heatmaps models
echo ""

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo ""
fi

# Run migrations
echo "Running database migrations..."
alembic upgrade head
echo ""

# Seed database (optional)
read -p "Seed database with sample data? (y/n): " SEED
if [ "$SEED" = "y" ] || [ "$SEED" = "Y" ]; then
    echo "Seeding database..."
    python seed_db.py 10
    echo ""
fi

echo "========================================"
echo "Starting LeafDoc API..."
echo "========================================"
echo ""
echo "API will be available at:"
echo "  - http://localhost:8000"
echo "  - Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
