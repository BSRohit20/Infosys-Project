# AI-Driven Guest Experience Personalization System for Hospitality

A comprehensive FastAPI-based hospitality management system with AI-powered sentiment analysis and personalized guest recommendations.

## Features

- **AI-Powered Sentiment Analysis**: Real-time sentiment analysis of guest feedback using Hugging Face DistilBERT
- **Personalized Recommendations**: AI-driven recommendations for amenities, dining, and activities based on CRM data
- **Real-time Alerts**: Slack webhook integration for negative sentiment detection
- **Dual User Interface**: Separate dashboards for admin analytics and guest recommendations
- **Beautiful UI**: Modern, responsive templates with Jinja2

## Tech Stack

- **Backend**: FastAPI
- **Frontend**: Jinja2 Templates, HTML/CSS/JavaScript
- **AI/ML**: Hugging Face Transformers (DistilBERT)
- **Database**: JSON files (mock CRM data)
- **Alerts**: Slack Webhooks
- **Authentication**: Python-JOSE with JWT tokens
- **Password Hashing**: Passlib with bcrypt
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Web Server**: Uvicorn (ASGI server)
- **HTTP Client**: Requests
- **Environment Management**: Python-dotenv
- **File Operations**: Aiofiles
- **Real-time Communication**: WebSockets

## Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/BSRohit20/Infosys-Project.git
   cd Infosys-Project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   - Create a `.env` file in the root directory
   - Configure necessary variables for your local setup

6. **Run the application**
   - Using convenience scripts:
     ```
     # Windows CMD
     run_local.bat
     
     # PowerShell
     ./run_local.ps1
     ```
   - Or run directly:
     ```
     python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
     ```

7. **Access the application**
   - Open your browser to [http://localhost:8000](http://localhost:8000)
   - Use the admin interface to create guest accounts and manage the system
   ```bash
   uvicorn app.main:app --reload
   ```

## Users

- **Admin**: View analytics, alerts, and system management
- **Guest**: Receive personalized recommendations and submit feedback

## API Endpoints

- `/` - Guest dashboard
- `/admin` - Admin dashboard
- `/api/feedback` - Feedback submission and analysis
- `/api/recommendations` - Personalized recommendations
- `/api/analytics` - System analytics

## Environment Variables

```
SLACK_WEBHOOK_URL=your_slack_webhook_url
HF_API_TOKEN=your_hugging_face_token
SECRET_KEY=your_secret_key
```
