import random
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
    market_type: str # 'bookmaker' ya 'fancy'
    selection: str
    amount: float
    odds: float

@app.get("/matches")
def get_matches():
    # Asli Lotus365 jaisa data structure
    return {
        "balance": user_data["balance"],
        "active_bets": user_data["active_bets"],
        "matches": [
            {
                "id": 1, "t1": "India", "t2": "Pakistan",
                "score": f"{random.randint(145, 155)}/4", "overs": "17.2",
                "b1": 1.44, "l1": 1.46, "b2": 2.80, "l2": 2.85,
                "fancy_ques": "India 20 Over Runs", "fancy_yes": 182, "fancy_no": 184
            }
        ]
    }

@app.post("/place-bet")
def place_bet(bet: BetRequest):
    if bet.amount > user_data["balance"]:
        raise HTTPException(status_code=400, detail="Balance kam hai!")
    
    user_data["balance"] -= bet.amount
    bet_id = len(user_data["active_bets"]) + 1
    user_data["active_bets"].append({
        "id": bet_id, "selection": bet.selection, 
        "amt": bet.amount, "odds": bet.odds
    })
    return {"message": "Bet Done!", "balance": user_data["balance"]}

@app.post("/cash-out/{bet_id}")
def cash_out(bet_id: int):
    for i, b in enumerate(user_data["active_bets"]):
        if b["id"] == bet_id:
            # 5% cut karke cashout
            refund = b["amt"] * 0.95
            user_data["balance"] += refund
            user_data["active_bets"].pop(i)
            return {"message": f"Cashout Success! ₹{refund:.2f} wapas mile"}
    return {"message": "Error"}
