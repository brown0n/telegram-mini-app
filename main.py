from fastapi import FastAPI, Request
import sqlite3

app = FastAPI()

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect("bets.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        match TEXT,
                        team TEXT,
                        amount INTEGER)''')
    conn.commit()
    conn.close()

@app.post("/place_bet/")
async def place_bet(request: Request):
    data = await request.json()
    user_id = data["user"]["id"]
    match = data["match"]
    team = data["team"]
    amount = data["amount"]

    conn = sqlite3.connect("bets.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bets (user_id, match, team, amount) VALUES (?, ?, ?, ?)", 
                   (user_id, match, team, amount))
    conn.commit()
    conn.close()
    
    return {"status": "success", "message": "Ставка принята"}

# Запуск сервера
if __name__ == "__main__":
    import uvicorn
    init_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)
