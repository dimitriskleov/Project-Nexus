from fastapi import FastAPI
import random

app = FastAPI()

# Load jokes from the list.txt file
def load_jokes():
    with open("list.txt", "r") as file:
        jokes = file.readlines()
    return [joke.strip() for joke in jokes]

# Update the path to match the one you're trying to use
@app.get("/api/v1/random_joke/main")
async def get_random_joke():
    jokes = load_jokes()
    joke = random.choice(jokes)
    return {"joke": joke}
