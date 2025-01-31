from fastapi import FastAPI
import random

app = FastAPI()

@app.get("/api/dice_api")
async def roll_dice():
    dice_roll = random.randint(1, 6)
    return {"dice_roll": dice_roll}
