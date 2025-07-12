#!/bin/bash
# Render build script for Python 3.11 compatibility

set -e

echo "🔧 Setting up Python 3.11 environment..."

# Ensure we're using Python 3.11
python3.11 --version || {
    echo "❌ Python 3.11 not available"
    exit 1
}

echo "📦 Installing build tools..."
python3.11 -m pip install --upgrade pip==24.0
python3.11 -m pip install setuptools==69.5.1 wheel==0.43.0

echo "📋 Installing application dependencies..."
python3.11 -m pip install -r requirements-minimal.txt

echo "✅ Build completed successfully!"
