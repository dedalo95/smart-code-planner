.PHONY: help install run test lint format clean docker-build docker-run setup validate

# Default target
help:
	@echo "🤖 Smart Code Planner - Available Commands:"
	@echo ""
	@echo "  setup       - Initial setup (install deps, create .env, etc.)"
	@echo "  install     - Install dependencies with Poetry"
	@echo "  run         - Run the Streamlit application"
	@echo "  test        - Run tests"
	@echo "  lint        - Run linting (flake8, mypy)"
	@echo "  format      - Format code (black, isort)"
	@echo "  clean       - Clean up cache files"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run  - Run with Docker Compose"
	@echo "  validate    - Validate project setup"
	@echo "  help        - Show this help message"

# Initial setup
setup:
	@echo "🚀 Setting up Smart Code Planner..."
	@./setup.sh

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	poetry install

# Run the application
run:
	@echo "🤖 Starting Smart Code Planner..."
	@echo "   Access at: http://localhost:8501"
	@poetry run streamlit run app.py

# Run tests
test:
	@echo "🧪 Running tests..."
	poetry run pytest tests/ -v

# Run linting
lint:
	@echo "🔍 Running linting..."
	poetry run flake8 src/ tests/
	poetry run mypy src/

# Format code
format:
	@echo "✨ Formatting code..."
	poetry run black src/ tests/
	poetry run isort src/ tests/

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true

# Docker build
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -f docker/Dockerfile -t smart-code-planner .

# Docker run
docker-run:
	@echo "🐳 Running with Docker Compose..."
	docker-compose up --build

# Development server (with auto-reload)
dev:
	@echo "🔄 Starting development server..."
	@poetry run streamlit run app.py --server.runOnSave true

# Validate project setup
validate:
	@echo "🔍 Validating project setup..."
	@./validate.sh
