#!/bin/bash

# Smart Code Planner Setup Script
# This script helps set up the development environment

set -e

echo "🤖 Setting up Smart Code Planner..."

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is not installed. Please install Poetry first:"
    echo "   curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

echo "✅ Poetry found"

# Install dependencies
echo "📦 Installing dependencies..."
poetry install

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file from example..."
    cp .env.example .env
    echo "🔑 Please edit .env file and add your API keys!"
    echo "   Required: OPENAI_API_KEY"
    echo "   Optional: LANGCHAIN_API_KEY (for tracing)"
fi

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
poetry run pre-commit install

# Run tests to verify setup
echo "🧪 Running tests to verify setup..."
poetry run pytest tests/ -v

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run the application:"
echo "   poetry run streamlit run src/ui/streamlit_app.py"
echo ""
echo "Or use Docker:"
echo "   docker-compose up --build"
echo ""
echo "Happy coding! 🚀"
