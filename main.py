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
