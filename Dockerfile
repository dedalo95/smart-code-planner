# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.6.1

# Configure Poetry: disable virtualenv creation since we're in a container
RUN poetry config virtualenvs.create false

# Copy poetry files first for better layer caching
COPY pyproject.toml poetry.lock* ./

# Install dependencies directly to system Python
RUN poetry install --no-root --no-dev || poetry install --no-root

# Copy application code
COPY . .

# Install the current project if it's a package
RUN poetry install --only-root || true

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["poetry", "run", "streamlit", "run", "src/ui/streamlit_app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
