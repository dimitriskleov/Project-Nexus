from fastapi import FastAPI, HTTPException, Depends
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os
import base64
from typing import Dict

# API Key for authentication
API_KEY = "supersecretapikey"

def get_api_key(api_key: str):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

app = FastAPI()

# Generate a secure 256-bit key (should be stored securely)
SECRET_KEY = os.urandom(32)  # AES-256 key
IV = os.urandom(16)  # Initialization Vector

def encrypt_text(plain_text: str) -> str:
    # Pad the text to be AES block size compliant
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plain_text.encode()) + padder.finalize()
    
    # Encrypt using AES-256 in CBC mode
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(IV))
    encryptor = cipher.encryptor()
    encrypted_bytes = encryptor.update(padded_data) + encryptor.finalize()
    
    # Encode the result in base64 for easy transmission
    return base64.b64encode(IV + encrypted_bytes).decode()

@app.post("/encrypt")
def encrypt(data: Dict[str, str], api_key: str = Depends(get_api_key)):
    text = data.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")
    
    encrypted_text = encrypt_text(text)
    return {"encrypted": encrypted_text}
