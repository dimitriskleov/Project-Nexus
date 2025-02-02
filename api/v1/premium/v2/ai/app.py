from fastapi import FastAPI
from pydantic import BaseModel
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Initialize FastAPI app
app = FastAPI()

# Load GPT-2 model and tokenizer (this happens once when the app starts)
model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Route to handle the AI requests
class AIRequest(BaseModel):
    text: str

@app.post("/generate")
async def generate_text(request: AIRequest):
    # Prepare the input text
    input_text = request.text
    
    # Tokenize input text
    inputs = tokenizer.encode(input_text, return_tensors="pt")
    
    # Generate response using the GPT-2 model
    outputs = model.generate(inputs, max_length=150, num_return_sequences=1, no_repeat_ngram_size=2)
    
    # Decode the generated text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return {"generated_text": generated_text}

