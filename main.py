from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI() # <--- Ye line sabse zaroori hai

# CORS allow karne ke liye
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

matches = [
    {"id": 1, "match": "India vs Pakistan", "odds_1": 1.4, "odds_2": 2.8, "status": "Live"},
    {"id": 2, "match": "Australia vs England", "odds_1": 1.9, "odds_2": 1.9, "status": "Upcoming"}
]

user_data = {"username": "Nikhil", "balance": 5000.0}

class BetRequest(BaseModel):
    match_id: int
    team_selected: int
    amount: float

@app.get("/")
def home():
    return {"status": "API is working"}

@app.get("/matches")
def get_all_matches():
    return {"matches": matches}

@app.get("/balance")
def check_balance():
    return {"balance": user_data["balance"]}

@app.post("/place-bet")
def place_bet(bet: BetRequest):
    if bet.amount > user_data["balance"]:
        raise HTTPException(status_code=400, detail="Paisa kam hai!")
    user_data["balance"] -= bet.amount
    return {"status": "Bet lag gayi!", "new_balance": user_data["balance"]}
