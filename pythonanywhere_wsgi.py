"""
PythonAnywhere WSGI configuration file.
This configuration allows running the FastAPI application on PythonAnywhere's free tier.
"""

import os
import sys

# Add the app directory to the Python path
path = '/home/YOUR_USERNAME/infosys'
if path not in sys.path:
    sys.path.append(path)

# Import the FastAPI app
from app.main import app

# Create a WSGI application
from fastapi.middleware.wsgi import WSGIMiddleware

application = WSGIMiddleware(app)
