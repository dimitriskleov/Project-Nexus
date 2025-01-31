from fastapi import FastAPI
import random

app = FastAPI()

@app.get("/random_number")
async def get_random_number():
    random_num = random.randint(1, 100)
    return {"random_number": random_num}
