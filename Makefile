.PHONY: help dev test format lint migrate clean install docker-up docker-down

help:
	@echo "LeafDoc API - Available commands:"
	@echo "  make install     - Install dependencies"
	@echo "  make dev         - Run development server"
	@echo "  make test        - Run tests"
	@echo "  make format      - Format code with black and isort"
	@echo "  make lint        - Lint code with ruff"
	@echo "  make migrate     - Run database migrations"
	@echo "  make clean       - Clean up generated files"
	@echo "  make docker-up   - Start Docker containers"
	@echo "  make docker-down - Stop Docker containers"

install:
	pip install -r requirements.txt
	@echo "Creating storage directories..."
	-mkdir storage storage\\images storage\\heatmaps models 2>nul || echo Storage dirs created

dev:
	@echo "Starting development server..."
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	@echo "Running tests..."
	pytest -v --cov=app --cov-report=term-missing

test-fast:
	@echo "Running tests (fast)..."
	pytest -v

format:
	@echo "Formatting code..."
	black app/ tests/
	isort app/ tests/

lint:
	@echo "Linting code..."
	ruff check app/ tests/
	mypy app/

migrate:
	@echo "Running database migrations..."
	alembic upgrade head

migration:
	@echo "Creating new migration..."
	@if "$(msg)"=="" (echo Error: msg parameter required. Usage: make migration msg="description") else (alembic revision --autogenerate -m "$(msg)")

clean:
	@echo "Cleaning up..."
	-del /s /q *.pyc 2>nul
	-del /s /q __pycache__ 2>nul
	-del /q *.db 2>nul
	-rmdir /s /q .pytest_cache 2>nul
	-rmdir /s /q .mypy_cache 2>nul
	-rmdir /s /q htmlcov 2>nul
	-rmdir /s /q .ruff_cache 2>nul
	@echo "Cleaned!"

docker-up:
	@echo "Starting Docker containers..."
	docker-compose up -d

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-build:
	@echo "Building Docker image..."
	docker-compose build
