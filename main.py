import random
import httpx # Iske liye 'pip install httpx' karna hoga agar error aaye
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
    market_type: str
    selection: str
    amount: float
    odds: float

@app.get("/matches")
async def get_matches():
    # Asli Match Details (Aap inhe manually update kar sakte hain ya real API link kar sakte hain)
    # Filhal hum live tracking simulate kar rahe hain
    live_score = f"{random.randint(160, 190)}/{random.randint(2, 5)}"
    
    return {
        "balance": user_data["balance"],
        "active_bets": user_data["active_bets"],
        "matches": [
            {
                "id": 101, 
                "t1": "RCB", "t2": "CSK", 
                "score": live_score, 
                "overs": "18.4",
                "b1": 1.82, "l1": 1.84, 
                "b2": 2.10, "l2": 2.12,
                "fancy_ques": "RCB 20 Over Runs", 
                "fancy_yes": 195, "fancy_no": 197
            }
        ]
    }

@app.post("/place-bet")
def place_bet(bet: BetRequest):
    if bet.amount > user_data["balance"]:
        raise HTTPException(status_code=400, detail="Balance Low!")
    
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
            refund = b["amt"] * 0.98 # Lotus jaisa low commission
            user_data["balance"] += refund
            user_data["active_bets"].pop(i)
            return {"message": "Cashout Done"}
    return {"message": "Error"}
