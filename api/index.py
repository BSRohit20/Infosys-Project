import os
import sys

# Add the app directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Replace sentiment service import for deployment
import importlib.util
import app.services.sentiment_service as sentiment_module

# Use lightweight sentiment service for deployment
try:
    from app.services.sentiment_service_deployment import sentiment_service
    sentiment_module.sentiment_service = sentiment_service
    print("✅ Using lightweight sentiment service for deployment")
except ImportError:
    print("⚠️ Using default sentiment service")

from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL path
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Set response headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Route handling
        if path == '/' or path == '/api' or path == '/api/':
            response_data = {
                "message": "🏨 Nexus Hospitality System - API Working!",
                "status": "✅ ONLINE",
                "deployment": "vercel-serverless",
                "timestamp": "2025-07-11",
                "features": [
                    "✨ AI-Powered Sentiment Analysis",
                    "👥 Guest Management System", 
                    "📊 Admin Dashboard",
                    "⚡ Real-time Feedback Processing"
                ],
                "credentials": {
                    "admin": "admin / admin123",
                    "guests": ["rohit/abc123", "sam/sam123", "revanth/revanth123"]
                }
            }
        elif path == '/api/health':
            response_data = {
                "status": "healthy",
                "service": "nexus-hospitality", 
                "deployment": "vercel-production",
                "version": "1.0.0",
                "timestamp": "2025-07-11",
                "uptime": "operational"
            }
        elif path == '/api/test':
            response_data = {
                "test_status": "✅ SUCCESS",
                "api_working": True,
                "message": "API is functioning correctly!",
                "vercel_deployment": "operational",
                "response_time": "fast"
            }
        elif path == '/api/status':
            response_data = {
                "application": "Nexus Hospitality System",
                "environment": "production", 
                "status": "operational",
                "features_active": True,
                "ai_sentiment": "lightweight-mode",
                "database": "json-file-storage",
                "last_updated": "2025-07-11"
            }
        else:
            response_data = {
                "error": "Endpoint not found",
                "requested_path": path,
                "available_endpoints": [
                    "/api",
                    "/api/health", 
                    "/api/test",
                    "/api/status"
                ],
                "message": "Use one of the available endpoints above"
            }
        
        # Send JSON response
        self.wfile.write(json.dumps(response_data, indent=2).encode())
        
    def do_POST(self):
        # Handle POST requests
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response_data = {
            "message": "POST request received",
            "status": "success",
            "note": "Full application features available in main deployment"
        }
        
        self.wfile.write(json.dumps(response_data).encode())
