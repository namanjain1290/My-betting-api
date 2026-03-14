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

# User ka data (Ye server chalne tak save rahega)
user_data = {"balance": 5000.0}

class BetRequest(BaseModel):
    match_id: int
    team_selected: int
    amount: float

@app.get("/matches")
def get_matches():
    # Har baar naye scores aur odds generate honge (Asli feel ke liye)
    live_matches = [
        {
            "id": 1, 
            "t1": "India", "t2": "Pakistan", 
            "score": f"{random.randint(120, 180)}/{random.randint(1, 6)}",
            "overs": f"{random.randint(15, 19)}.{random.randint(1, 5)}",
            "o1": round(random.uniform(1.2, 2.5), 2), 
            "o2": round(random.uniform(2.6, 4.5), 2), 
            "status": "Live"
        },
        {
            "id": 2, 
            "t1": "Australia", "t2": "England", 
            "score": "0/0", "overs": "0.0",
            "o1": 1.9, "o2": 1.9, 
            "status": "Upcoming"
        }
    ]
    return {"matches": live_matches, "balance": user_data["balance"]}

@app.post("/place-bet")
def place_bet(bet: BetRequest):
    if bet.amount > user_data["balance"]:
        raise HTTPException(status_code=400, detail="Paisa kam hai!")
    
    # Randomly jeetna ya haarna (Logic)
    win = random.choice([True, False])
    
    # Hum 1.5x odds pakad lete hain generic trial ke liye
    if win:
        profit = bet.amount * 0.8 # 80% profit
        user_data["balance"] += profit
        return {"message": f"Mubarak ho! Aap ₹{profit} jeet gaye.", "new_balance": user_data["balance"]}
    else:
        user_data["balance"] -= bet.amount
        return {"message": f"Oho! Aap ₹{bet.amount} haar gaye.", "new_balance": user_data["balance"]}
