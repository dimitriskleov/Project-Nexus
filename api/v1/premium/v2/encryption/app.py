from fastapi import FastAPI, HTTPException, Depends

# API Key for authentication
API_KEY = "supersecretapikey"

def get_api_key(api_key: str):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

app = FastAPI()

# Custom simple encryption method using character mapping
ENCRYPTION_MAP = {
    "a": "@", "b": "8", "c": "(", "d": "#", "e": "3", "f": "!", "g": "6", "h": "4", "i": "1",
    "j": "?", "k": "<", "l": "7", "m": "M", "n": "N", "o": "0", "p": "%", "q": "Q", "r": "2",
    "s": "$", "t": "+", "u": "U", "v": "V", "w": "W", "x": "*", "y": "Y", "z": "Z"
}

def encrypt_text(plain_text: str) -> str:
    encrypted_text = "".join(ENCRYPTION_MAP.get(char, char) for char in plain_text.lower())
    return encrypted_text

@app.post("/encrypt")
def encrypt(data: dict, api_key: str = Depends(get_api_key)):
    text = data.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")
    
    encrypted_text = encrypt_text(text)
    return {"encrypted": encrypted_text}
