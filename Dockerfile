FROM python:3.11-slim

# Install system dependencies for ML libraries
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy optimized requirements for deployment
COPY requirements-render.txt requirements.txt

# Install Python dependencies with optimizations for ML
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create cache directory for HuggingFace models
RUN mkdir -p /app/.cache

# Set environment variables for ML optimization
ENV PYTHONPATH=/app
ENV TRANSFORMERS_CACHE=/app/.cache
ENV HF_HOME=/app/.cache
ENV TOKENIZERS_PARALLELISM=false

# Expose port (Render uses $PORT)
EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/ || exit 1

# Start command optimized for Render
CMD ["sh", "-c", "python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create cache directory for Hugging Face models
RUN mkdir -p /app/.cache/huggingface

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
