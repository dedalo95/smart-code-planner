#!/bin/bash

# Simple run script for the Smart Code Planner

set -e

echo "🤖 Starting Smart Code Planner..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from example..."
    cp .env.example .env
    echo "🔑 Please edit .env file and add your OpenAI API key!"
    echo "   Then run this script again."
    exit 1
fi

# Check if OPENAI_API_KEY is set
if ! grep -q "OPENAI_API_KEY=sk-" .env 2>/dev/null; then
    echo "⚠️  Please add your OpenAI API key to the .env file!"
    echo "   Edit .env and set OPENAI_API_KEY=your_actual_key_here"
    exit 1
fi

echo "✅ Configuration looks good!"
echo "🚀 Starting Streamlit application..."
echo "   Access the app at: http://localhost:8501"
echo ""

# Run the application
echo "🚀 Starting Streamlit application..."
echo "   Access the app at: http://localhost:8501"
echo ""

# Use the main app launcher
poetry run streamlit run app.py
