from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 1. Dummy Data - Matches ki list
# 2026 ke trend ke hisab se humne odds set kiye hain
matches = [
    {"id": 1, "match": "India vs Pakistan", "odds_1": 1.4, "odds_2": 2.8, "status": "Live"},
    {"id": 2, "match": "Australia vs England", "odds_1": 1.9, "odds_2": 1.9, "status": "Upcoming"},
    {"id": 3, "match": "Real Madrid vs Barcelona", "odds_1": 2.1, "odds_2": 1.7, "status": "Live"}
]

# User ka wallet (Virtual money)
user_data = {"username": "Guest_User", "balance": 5000.0}

# Bet lagane ke liye structure
class BetRequest(BaseModel):
    match_id: int
    team_selected: int  # 1 for Team A, 2 for Team B
    amount: float

@app.get("/")
def home():
    return {
        "message": "Welcome to the Betting API",
        "user_balance": user_data["balance"],
        "endpoints": ["/matches", "/balance", "/place-bet"]
    }

@app.get("/matches")
def get_all_matches():
    return {"matches": matches}

@app.get("/balance")
def check_balance():
    return {"username": user_data["username"], "balance": user_data["balance"]}

@app.post("/place-bet")
def place_bet(bet: BetRequest):
    # Check if match exists
    match = next((m for m in matches if m["id"] == bet.match_id), None)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    # Check balance
    if bet.amount > user_data["balance"]:
        raise HTTPException(status_code=400, detail="Paisa kam hai! Recharge karein.")

    # Deduct money
    user_data["balance"] -= bet.amount
    
    selected_team_name = match["match"].split(" vs ")[bet.team_selected - 1]
    
    return {
        "status": "Bet Placed Successfully!",
        "team": selected_team_name,
        "amount": bet.amount,
        "new_balance": user_data["balance"]
    }
