from fastapi import FastAPI
import random

app = FastAPI()

# Function to read jokes from the file and store them in a list
def load_jokes():
    with open("list.txt", "r") as file:
        jokes = file.readlines()
    return [joke.strip() for joke in jokes]

# Route to get a random joke
@app.get("/random_joke")
async def get_random_joke():
    jokes = load_jokes()
    joke = random.choice(jokes)  # Pick a random joke
    return {"joke": joke}

# Route to get a specific joke by index
@app.get("/random_joke/{index}")
async def get_joke_by_index(index: int):
    jokes = load_jokes()
    if index < len(jokes):
        return {"joke": jokes[index]}
    else:
        return {"error": "Joke not found"}
