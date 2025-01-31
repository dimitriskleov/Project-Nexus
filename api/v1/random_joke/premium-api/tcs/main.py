from fastapi import FastAPI, HTTPException
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

@app.post("/store/")
async def store_text(request: TextRequest):
    """Store text and return a unique key."""
    text = request.text
    
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # Generate a unique key
    unique_key = generate_unique_key()
    
    # Save the text with the generated key
    stored_data[unique_key] = text
    
    return {"message": "Text stored successfully", "key": unique_key}

@app.get("/retrieve/{key}")
async def retrieve_text(key: str):
    """Retrieve text using the unique key."""
    text = stored_data.get(key)
    
    if not text:
        raise HTTPException(status_code=404, detail="Text not found for this key")
    
    return {"key": key, "text": text}

