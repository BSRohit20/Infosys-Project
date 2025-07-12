# Use Python 3.11.9 for ML compatibility
FROM python:3.11.9-slim

# Install system dependencies for ML libraries
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements-minimal.txt .

# Install Python dependencies with specific versions for compatibility
RUN pip install --no-cache-dir --upgrade pip==24.0 && \
    pip install --no-cache-dir setuptools==69.5.1 wheel==0.43.0 && \
    pip install --no-cache-dir -r requirements-minimal.txt

# Copy application code
COPY . .

# Create cache directory for HuggingFace models
RUN mkdir -p /app/.cache/huggingface

# Set environment variables for ML optimization
ENV PYTHONPATH=/app
ENV TRANSFORMERS_CACHE=/app/.cache
ENV HF_HOME=/app/.cache
ENV TOKENIZERS_PARALLELISM=false
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose port (Render will set $PORT)
EXPOSE 10000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-10000}/health || exit 1

# Start command optimized for Render
CMD ["sh", "-c", "python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
