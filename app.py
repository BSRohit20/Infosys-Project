# Hugging Face Spaces deployment file
import gradio as gr
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.main import app as fastapi_app

# Create Gradio interface for easy ML demo
def analyze_feedback(text):
    """Simple interface for sentiment analysis"""
    from app.services.sentiment_service import sentiment_service
    import asyncio
    
    result = asyncio.run(sentiment_service.analyze_sentiment(text))
    
    return {
        "Sentiment": result["sentiment"].title(),
        "Confidence": f"{result['confidence']:.2%}",
        "Model": result.get("model", "DistilBERT")
    }

# Gradio interface
iface = gr.Interface(
    fn=analyze_feedback,
    inputs=gr.Textbox(label="Guest Feedback", placeholder="Enter guest feedback here..."),
    outputs=gr.JSON(label="Sentiment Analysis Result"),
    title="🏨 AI Guest Feedback Analyzer",
    description="Real-time sentiment analysis for hospitality feedback using DistilBERT",
    examples=[
        ["The hotel was absolutely amazing! Great service and beautiful rooms."],
        ["The room was dirty and the staff was rude. Very disappointing experience."],
        ["Average stay, nothing special but adequate for the price."]
    ]
)

# Mount FastAPI app
app = gr.mount_gradio_app(fastapi_app, iface, path="/demo")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
