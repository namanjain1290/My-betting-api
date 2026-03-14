from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

user_data = {"balance": 5000.0, "active_bets": []}

class BetRequest(BaseModel):
    match_id: int
    market_type: str
    selection: str
    amount: float
    odds: float

@app.get("/")
def home():
    return {"status": "Online", "msg": "Nikhil Exchange Live"}

@app.get("/matches")
def get_matches():
    # Simulation for real-time feel
    return {
        "balance": user_data["balance"],
        "active_bets": user_data["active_bets"],
        "matches": [
            {
                "id": 101,
                "t1": "RCB", "t2": "CSK",
                "score": f"{random.randint(165, 185)}/{random.randint(2, 5)}",
                "overs": f"18.{random.randint(1, 5)}",
                "b1": 1.85, "l1": 1.87, 
                "b2": 2.12, "l2": 2.15,
                "fancy_ques": "RCB 20 Over Runs",
                "fancy_yes": 196, "fancy_no": 198
            }
        ]
    }

@app.post("/place-bet")
def place_bet(bet: BetRequest):
    if bet.amount > user_data["balance"]:
        raise HTTPException(status_code=400, detail="Low Balance")
    user_data["balance"] -= bet.amount
    user_data["active_bets"].append({
        "id": len(user_data["active_bets"]) + 1,
        "selection": bet.selection,
        "amt": bet.amount,
        "odds": bet.odds
    })
    return {"message": "Success", "balance": user_data["balance"]}

@app.post("/cash-out/{bet_id}")
def cash_out(bet_id: int):
    for i, b in enumerate(user_data["active_bets"]):
        if b["id"] == bet_id:
            refund = b["amt"] * 0.98
            user_data["balance"] += refund
            user_data["active_bets"].pop(i)
            return {"message": "Cashout Success"}
    return {"message": "Error"}
