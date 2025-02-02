from fastapi import FastAPI
from pydantic import BaseModel
import requests

# Initialize FastAPI app
app = FastAPI()

# Define the input data model
class AIRequest(BaseModel):
    text: str

# API URL (external AI endpoint)
external_api_url = "https://project-nexus-xi.vercel.app/api/v1/premium/v2/ai"

# Route to handle the AI requests
@app.post("/generate")
async def generate_text(request: AIRequest):
    # Prepare data to send to the external AI API
    payload = {
        "text": request.text
    }

    # Send POST request to the external API
    response = requests.post(external_api_url, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Return the response from the external API
        return {"generated_text": response.json()}
    else:
        # Handle errors if any
        return {"error": "Failed to get a response from the external AI API"}

