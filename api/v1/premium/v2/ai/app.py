from fastapi import FastAPI
from pydantic import BaseModel
import gpt_2_simple as gpt2
import os

# Initialize FastAPI app
app = FastAPI()

# Load the GPT-2 model once at startup
MODEL_NAME = "124M"  # You can choose other model sizes like "355M", "774M", etc.
gpt2.load_gpt2(model_name=MODEL_NAME)

# Route to handle the AI requests
class AIRequest(BaseModel):
    text: str

@app.post("/generate")
async def generate_text(request: AIRequest):
    # Prepare the input text
    input_text = request.text
    
    # Start a TensorFlow session and generate the text
    sess = gpt2.start_tf_sess()
    response = gpt2.generate(sess, model_name=MODEL_NAME, prefix=input_text, return_as_list=True, length=150)

    # Return the generated text
    return {"generated_text": response[0]}
