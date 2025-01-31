from fastapi import FastAPI
import random

app = FastAPI()

# List of jokes embedded directly in the code
jokes = [
    "Why did the math book look so sad? It had too many problems.",
    "What do you get when you cross a snowman with a vampire? Frostbite!",
    "Why don’t skeletons fight each other? They don’t have the guts.",
    "How does a penguin build its house? Igloos it together!",
    "Why did the bicycle fall over? It was two-tired.",
    "What do you call fake spaghetti? An impasta!",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "What do you call cheese that isn’t yours? Nacho cheese!",
    "Why was the computer cold? It left its Windows open.",
    "Why did the golfer bring two pairs of pants? In case he got a hole in one.",
    "What do you get when you cross an elephant with a rhinoceros? Elephino!",
    "Why don’t oysters share their pearls? Because they’re shellfish!",
    "What do you call a bear with no teeth? A gummy bear.",
    "Why don’t eggs tell jokes? They might crack up!",
    "What did the grape do when it got stepped on? Nothing, it just let out a little wine!",
    "Why don’t skeletons use cell phones? They don’t have the nerve!",
    "What’s brown and sticky? A stick!",
    "Why did the coffee file a police report? It got mugged!",
    "How do cows stay up to date with current events? They read the moos-paper!",
    "What did one plate say to the other plate? Lunch is on me!"
]

# Endpoint to get a random joke
@app.get("/api/v1/random_joke/main")
async def get_random_joke():
    joke = random.choice(jokes)  # Select a random joke from the list
    return {"joke": joke}
