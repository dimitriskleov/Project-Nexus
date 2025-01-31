from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel
import random
import string

# Initialize FastAPI app
app = FastAPI()

# In-memory storage (this will reset when the app restarts)
stored_data = {}

# Pydantic model to handle incoming JSON data
class TextRequest(BaseModel):
    text: str

def generate_unique_key() -> str:
    """Generate a random string key."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# Call the external endpoint
def get_external_data():
    url = "https://project-nexus-xi.vercel.app/api/v1/random_joke/premium-api/tcs/main"
    
    try:
        # Send a GET request to the external API
        response = requests.get(url)
        
        # If the request was successful, return the JSON data
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Error retrieving data from external API.")
    
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request error: {e}")

@app.post("/store/")
async def store_text(request: TextRequest):
    """Store text and return a unique key."""
    text = request.text
    
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # Generate a unique key
    unique_key = generate_unique_key()
    
    # Save the text with the unique key
    stored_data[unique_key] = text
    
    return {"message": "Text stored successfully", "key": unique_key}

@app.get("/retrieve/{key}")
async def retrieve_text(key: str):
    """Retrieve text using the unique key."""
    text = stored_data.get(key)
    
    if not text:
        raise HTTPException(status_code=404, detail="Text not found for this key")
    
    return {"key": key, "text": text}

@app.get("/external-data/")
async def external_data():
    """Endpoint to call external API and return data."""
    data = get_external_data()  # Call external API to get data
    return {"external_data": data}
