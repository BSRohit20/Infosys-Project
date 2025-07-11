# Render CLI Deployment Guide

## 🚀 Option 1: Deploy with Render CLI (Fastest)

### Install Render CLI:

**On Windows:**
```powershell
# Download the CLI binary
Invoke-WebRequest -Uri "https://github.com/render-oss/cli/releases/latest/download/cli_windows_amd64.zip" -OutFile "render-cli.zip"
Expand-Archive render-cli.zip -DestinationPath .
# Move to PATH or use directly: ./render.exe
```

**On macOS (Homebrew):**
```bash
brew update
brew install render
```

**On Linux:**
```bash
curl -L https://github.com/render-oss/cli/releases/latest/download/cli_linux_amd64.zip -o render.zip
unzip render.zip
sudo mv render /usr/local/bin/render
```

### Deploy directly from command line:
```bash
# Login to Render
render login

# Deploy your service (interactive)
render services

# Or trigger deploy directly
render deploys create [SERVICE_ID]
```

## 🌐 Option 2: Deploy via Web Dashboard (Recommended for first time)

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect Infosys-Project repository
5. Use the build settings from render.yaml

## 🔧 Option 3: Infrastructure as Code (Current Setup)

Your project already includes `render.yaml` which automatically configures:
- Build commands
- Start commands  
- Environment variables
- Disk storage for ML models

Just connect the repo and Render reads the YAML file automatically!

## ⚡ Quick Deploy Commands:

```bash
# Method 1: CLI (after installing)
render login
render services  # Select your service to deploy

# Method 2: Git-based (current setup)
git add . && git commit -m "Deploy" && git push
# Then connect repo in Render dashboard

# Method 3: One-click with YAML
# Just connect GitHub repo - render.yaml handles everything!
```
