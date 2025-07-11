# Render.com Deployment Guide

## Quick Setup Steps:

1. **Push to GitHub** (if not already done)
2. **Connect to Render:**
   - Go to [render.com](https://render.com)
   - Connect your GitHub account
   - Select your repository: `BSRohit20/Infosys-Project`

3. **Environment Variables to set in Render Dashboard:**
   ```
   SECRET_KEY=your-secret-key-here
   HF_API_TOKEN=your-huggingface-token (optional)
   SLACK_WEBHOOK_URL=your-slack-webhook (optional)
   ENVIRONMENT=production
   ```

4. **Render will automatically:**
   - Detect the `render.yaml` configuration
   - Build using the Dockerfile
   - Install ML dependencies
   - Deploy your app

## Expected Performance:
- **Build Time:** 3-5 minutes (first time)
- **Model Loading:** 30-60 seconds
- **Memory Usage:** ~400MB (within 512MB limit)
- **Response Time:** 1-3 seconds for ML inference

## Deployment URL:
Your app will be available at: `https://ai-hospitality-system.onrender.com`

## Notes:
- Free tier sleeps after 15 mins of inactivity
- First request after sleep takes 30-60s (cold start + model loading)
- Models are cached between requests for faster inference
