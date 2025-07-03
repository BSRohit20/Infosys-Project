import logging
from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import time
from dotenv import load_dotenv

from app.api import auth
from app.api.feedback_api import router as feedback_api_router
from app.api.recommendations_api import router as recommendations_api_router  
from app.api.analytics_api import router as analytics_api_router
from app.api.admin_api import router as admin_api_router
from app.api.auth import get_current_user, require_auth, require_admin, require_staff
from app.services.auth_service import auth_service
from app.services.sentiment_service import sentiment_service
from app.services.recommendation_service import recommendation_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="AI-Driven Guest Experience Personalization System",
    description="A comprehensive hospitality management system with AI-powered sentiment analysis and personalized recommendations",
    version="1.0.0"
)

# Add CORS middleware for proper cookie handling
# In production, allow specific origins or use * for all
is_prod = os.getenv("ENVIRONMENT", "development") == "production"
if is_prod:
    # Allow all origins in production (or specify your domain)
    origins = ["*"]
else:
    # Local development origins
    origins = os.getenv("CORS_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"🔍 Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"✅ Response: {response.status_code} in {process_time:.4f}s")
    return response

# Mount static files
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

# Set up templates
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(admin_api_router, prefix="/api/admin", tags=["admin"])

# Include new AI-powered API routers
app.include_router(feedback_api_router, tags=["feedback-ai"])
app.include_router(recommendations_api_router, tags=["recommendations-ai"])
app.include_router(analytics_api_router, tags=["analytics-ai"])

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "AI-Driven Guest Experience System is running",
        "version": "1.0.0"
    }

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Root redirect - check authentication and redirect appropriately"""
    try:
        user = get_current_user(request)
        if user:
            if user.role == 'admin':
                return RedirectResponse(url="/admin", status_code=302)
            else:
                return RedirectResponse(url="/dashboard", status_code=302)
    except:
        pass
    
    return RedirectResponse(url="/login", status_code=302)

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, user: auth.User = Depends(require_admin)):
    """Admin dashboard with AI analytics"""
    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "current_user": user
    })

@app.get("/admin/add-guest", response_class=HTMLResponse)
async def add_guest_page(request: Request, user: auth.User = Depends(require_admin)):
    """Admin page to add new guest accounts"""
    return templates.TemplateResponse("add_guest.html", {
        "request": request,
        "current_user": user
    })

@app.get("/dashboard", response_class=HTMLResponse)
async def guest_dashboard(request: Request, user: auth.User = Depends(require_auth)):
    """Guest dashboard with personalized recommendations"""
    return templates.TemplateResponse("guest_dashboard.html", {
        "request": request,
        "current_user": user
    })

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    try:
        # If already logged in, redirect to appropriate dashboard
        try:
            user = get_current_user(request)
            if user:
                if user.role == 'admin':
                    return RedirectResponse(url="/admin", status_code=302)
                else:
                    return RedirectResponse(url="/dashboard", status_code=302)
        except:
            pass
        
        return templates.TemplateResponse("login.html", {"request": request})
    except Exception as e:
        logger.error(f"Error loading login template: {e}")
        # Return a simple HTML page if template loading fails
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head><title>Login - AI Guest Experience</title></head>
        <body style="font-family: Arial, sans-serif; max-width: 400px; margin: 100px auto; padding: 20px;">
            <h1>AI Guest Experience System</h1>
            <h2>Login</h2>
            <form action="/login" method="post">
                <div style="margin-bottom: 15px;">
                    <label>Username:</label><br>
                    <input type="text" name="username" required style="width: 100%; padding: 8px; margin-top: 5px;">
                </div>
                <div style="margin-bottom: 15px;">
                    <label>Password:</label><br>
                    <input type="password" name="password" required style="width: 100%; padding: 8px; margin-top: 5px;">
                </div>
                <button type="submit" style="background: #2563eb; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">Login</button>
            </form>
            <p style="margin-top: 20px; font-size: 14px; color: #666;">
                Demo accounts:<br>
                Admin: admin / admin123<br>
                Guest: guest_001 / guest123
            </p>
        </body>
        </html>
        """)

@app.post("/login")
async def login_form_handler(username: str = Form(...), password: str = Form(...)):
    """Handle login form submission"""
    try:
        # Authenticate user
        user = auth_service.authenticate_user(username, password)
        if not user:
            # Return to login page with error
            return HTMLResponse(content=f"""
            <!DOCTYPE html>
            <html>
            <head><title>Login Failed</title></head>
            <body style="font-family: Arial, sans-serif; max-width: 400px; margin: 100px auto; padding: 20px;">
                <div style="background: #fee; border: 1px solid #fcc; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                    <strong>Login Failed:</strong> Invalid username or password
                </div>
                <a href="/login" style="color: #2563eb;">← Back to Login</a>
            </body>
            </html>
            """, status_code=401)
        
        # Create session
        session = auth_service.create_session(user)
        
        # Redirect to appropriate dashboard
        if user.role == 'admin':
            response = RedirectResponse(url="/admin", status_code=302)
        else:
            response = RedirectResponse(url="/dashboard", status_code=302)
        
        # Set session cookie with localhost-compatible settings
        response.set_cookie(
            key="session_token",
            value=session.session_token,
            max_age=86400,  # 24 hours
            path="/",       # Explicitly set path
            httponly=False, # Allow JavaScript access
            secure=False,   # Allow on HTTP for local development
            samesite="lax"  # More compatible than "none" for localhost
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        return HTMLResponse(content=f"""
        <!DOCTYPE html>
        <html>
        <head><title>Login Error</title></head>
        <body style="font-family: Arial, sans-serif; max-width: 400px; margin: 100px auto; padding: 20px;">
            <div style="background: #fee; border: 1px solid #fcc; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                <strong>Error:</strong> {str(e)}
            </div>
            <a href="/login" style="color: #2563eb;">← Back to Login</a>
        </body>
        </html>
        """, status_code=500)

@app.get("/admin/analytics", response_class=HTMLResponse)
async def admin_analytics(request: Request, user: auth.User = Depends(require_admin)):
    """Admin analytics page with detailed AI insights"""
    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "current_user": user
    })

@app.get("/recommendations", response_class=HTMLResponse)
async def recommendations_page(request: Request, user: auth.User = Depends(require_auth)):
    """Dedicated recommendations page"""
    return templates.TemplateResponse("recommendations.html", {
        "request": request,
        "current_user": user
    })

@app.get("/feedback", response_class=HTMLResponse)
async def feedback_page(request: Request, user: auth.User = Depends(require_auth)):
    """Dedicated feedback page"""
    return templates.TemplateResponse("feedback.html", {
        "request": request,
        "current_user": user
    })

@app.get("/concierge", response_class=HTMLResponse)
async def concierge_page(request: Request, user: auth.User = Depends(require_auth)):
    """Contact concierge page"""
    return templates.TemplateResponse("concierge.html", {
        "request": request,
        "current_user": user
    })

@app.get("/bookings", response_class=HTMLResponse)
async def bookings_page(request: Request, user: auth.User = Depends(require_auth)):
    """View bookings page"""
    return templates.TemplateResponse("bookings.html", {
        "request": request,
        "current_user": user
    })

@app.get("/logout")
async def logout(request: Request):
    """Logout and redirect to login page"""
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("session_token")
    return response

@app.get("/guest/{guest_id}", response_class=HTMLResponse)
async def guest_profile(request: Request, guest_id: str, user: auth.User = Depends(require_staff)):
    """Guest profile page - Admin/Staff only"""
    return templates.TemplateResponse("guest_profile.html", {
        "request": request, 
        "guest_id": guest_id,
        "user": user
    })

@app.get("/admin/alerts", response_class=HTMLResponse)
async def alerts_page(request: Request, user: auth.User = Depends(require_staff)):
    """Alerts and notifications page - Admin/Staff only"""
    return templates.TemplateResponse("alerts.html", {
        "request": request,
        "user": user
    })

@app.get("/admin/analytics", response_class=HTMLResponse)
async def analytics_page(request: Request, user: auth.User = Depends(require_staff)):
    """Advanced analytics page - Admin/Staff only"""
    return templates.TemplateResponse("analytics.html", {
        "request": request,
        "user": user
    })

@app.get("/admin/settings", response_class=HTMLResponse)
async def settings_page(request: Request, user: auth.User = Depends(require_admin)):
    """Settings and configuration page - Admin only"""
    return templates.TemplateResponse("settings.html", {
        "request": request,
        "user": user
    })

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "AI-Driven Guest Experience System is running",
        "version": "1.0.0"
    }

@app.get("/test")
async def test_route():
    """Simple test route"""
    return {"message": "Server is working!", "status": "ok"}

@app.get("/test-auth", response_class=HTMLResponse)
async def test_auth_page(request: Request):
    """Test page to debug authentication issues"""
    session_token = request.cookies.get('session_token')
    user = get_current_user(request)
    
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Authentication Test</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }}
            .status {{ padding: 15px; margin: 10px 0; border-radius: 5px; }}
            .success {{ background: #d4edda; border: 1px solid #c3e6cb; color: #155724; }}
            .error {{ background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }}
            .info {{ background: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; }}
            button {{ padding: 10px 20px; margin: 5px; border: none; border-radius: 5px; cursor: pointer; }}
            .btn-primary {{ background: #007bff; color: white; }}
            .btn-success {{ background: #28a745; color: white; }}
            .btn-danger {{ background: #dc3545; color: white; }}
            pre {{ background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        </style>
    </head>
    <body>
        <h1>🔍 Authentication Debug Test</h1>
        
        <div class="status {'success' if user else 'error'}">
            <h3>Authentication Status:</h3>
            <p><strong>Status:</strong> {'✅ AUTHENTICATED' if user else '❌ NOT AUTHENTICATED'}</p>
            <p><strong>Session Token:</strong> {session_token or 'None'}</p>
            <p><strong>User:</strong> {user.username if user else 'None'}</p>
            <p><strong>Role:</strong> {user.role if user else 'None'}</p>
        </div>

        <div class="info">
            <h3>Browser Cookies:</h3>
            <pre id="cookies">Loading...</pre>
        </div>

        <h3>Test Actions:</h3>
        <button class="btn-primary" onclick="testLogin()">🔐 Test Login (Admin)</button>
        <button class="btn-success" onclick="testDashboard()">📊 Test Dashboard Access</button>
        <button class="btn-danger" onclick="clearCookies()">🗑️ Clear Cookies</button>
        <button class="btn-primary" onclick="location.reload()">🔄 Refresh</button>

        <div id="results"></div>

        <script>
            // Display current cookies
            document.getElementById('cookies').textContent = document.cookie || 'No cookies found';

            async function testLogin() {{
                try {{
                    const response = await fetch('/api/auth/login', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ username: 'admin', password: 'admin123' }})
                    }});
                    
                    const data = await response.json();
                    
                    if (response.ok) {{
                        showResult('✅ Login successful! Cookie should be set.', 'success');
                        setTimeout(() => location.reload(), 1000);
                    }} else {{
                        showResult('❌ Login failed: ' + data.detail, 'error');
                    }}
                }} catch (error) {{
                    showResult('❌ Login error: ' + error.message, 'error');
                }}
            }}

            async function testDashboard() {{
                try {{
                    const response = await fetch('/dashboard');
                    if (response.ok) {{
                        showResult('✅ Dashboard access successful!', 'success');
                    }} else {{
                        const text = await response.text();
                        showResult('❌ Dashboard access failed: ' + text, 'error');
                    }}
                }} catch (error) {{
                    showResult('❌ Dashboard error: ' + error.message, 'error');
                }}
            }}

            function clearCookies() {{
                document.cookie = 'session_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
                showResult('🗑️ Cookies cleared', 'info');
                setTimeout(() => location.reload(), 1000);
            }}

            function showResult(message, type) {{
                const div = document.createElement('div');
                div.className = 'status ' + type;
                div.innerHTML = '<p>' + message + '</p>';
                document.getElementById('results').appendChild(div);
            }}

            // Auto-refresh cookies display every 2 seconds
            setInterval(() => {{
                document.getElementById('cookies').textContent = document.cookie || 'No cookies found';
            }}, 2000);
        </script>
    </body>
    </html>
    """)

@app.get("/test-localstorage-auth", response_class=HTMLResponse)
async def test_localstorage_auth():
    """Alternative auth test using localStorage instead of cookies"""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>LocalStorage Auth Test</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            .status { padding: 15px; margin: 10px 0; border-radius: 5px; }
            .success { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
            .error { background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }
            .info { background: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; }
            button { padding: 10px 20px; margin: 5px; border: none; border-radius: 5px; cursor: pointer; }
            .btn-primary { background: #007bff; color: white; }
            .btn-success { background: #28a745; color: white; }
            input { padding: 8px; margin: 5px; border: 1px solid #ccc; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>🔧 Alternative Auth Test (LocalStorage)</h1>
        
        <div class="info">
            <h3>Manual Login Test:</h3>
            <input type="text" id="username" placeholder="Username" value="admin">
            <input type="password" id="password" placeholder="Password" value="admin123">
            <button class="btn-primary" onclick="login()">Login</button>
        </div>

        <div class="info">
            <h3>Current Auth Status:</h3>
            <pre id="authStatus">Click "Check Status" to see current authentication</pre>
            <button class="btn-success" onclick="checkAuthStatus()">Check Status</button>
        </div>

        <div class="info">
            <h3>Dashboard Test:</h3>
            <button class="btn-primary" onclick="testDashboardAccess()">Test Dashboard Access</button>
        </div>

        <div id="results"></div>

        <script>
            async function login() {
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;
                
                try {
                    const response = await fetch('/api/auth/login', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ username, password })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        showResult('✅ Login API successful: ' + JSON.stringify(data), 'success');
                        checkAuthStatus();
                    } else {
                        showResult('❌ Login failed: ' + data.detail, 'error');
                    }
                } catch (error) {
                    showResult('❌ Login error: ' + error.message, 'error');
                }
            }

            async function checkAuthStatus() {
                try {
                    const response = await fetch('/api/auth/status');
                    const data = await response.json();
                    
                    document.getElementById('authStatus').textContent = JSON.stringify(data, null, 2);
                    
                    if (data.authenticated) {
                        showResult('✅ Authentication status: AUTHENTICATED as ' + data.user.username, 'success');
                    } else {
                        showResult('❌ Authentication status: NOT AUTHENTICATED', 'error');
                    }
                } catch (error) {
                    showResult('❌ Auth status error: ' + error.message, 'error');
                }
            }

            async function testDashboardAccess() {
                try {
                    const response = await fetch('/dashboard');
                    
                    if (response.ok) {
                        showResult('✅ Dashboard access: SUCCESS', 'success');
                    } else {
                        const text = await response.text();
                        showResult('❌ Dashboard access: FAILED - ' + text, 'error');
                    }
                } catch (error) {
                    showResult('❌ Dashboard error: ' + error.message, 'error');
                }
            }

            function showResult(message, type) {
                const div = document.createElement('div');
                div.className = 'status ' + type;
                div.innerHTML = '<p>' + message + '</p>';
                document.getElementById('results').appendChild(div);
            }

            // Check status on page load
            window.onload = () => {
                checkAuthStatus();
            };
        </script>
    </body>
    </html>
    """)

@app.get("/debug/cookies")
async def debug_cookies(request: Request):
    """Debug endpoint to see what cookies are being received"""
    cookies = request.cookies
    headers = dict(request.headers)
    return {
        "cookies": cookies,
        "headers": headers,
        "cookie_header": headers.get("cookie", "No cookie header found")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
