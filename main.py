from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Any, Dict
import sqlite3, json, uvicorn

app = FastAPI()

def init_db():
    with sqlite3.connect("game_save.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS saves (user_id TEXT PRIMARY KEY, data TEXT)")

init_db()

class GameState(BaseModel):
    user_id: str
    data: Dict[str, Any]

@app.post("/api/save")
async def save_game(state: GameState):
    with sqlite3.connect("game_save.db") as conn:
        conn.execute("INSERT OR REPLACE INTO saves VALUES (?, ?)", (state.user_id, json.dumps(state.data)))
    return {"status": "success"}

@app.get("/api/load/{user_id}")
async def load_game(user_id: str):
    with sqlite3.connect("game_save.db") as conn:
        row = conn.execute("SELECT data FROM saves WHERE user_id = ?", (user_id,)).fetchone()
    return {"data": json.loads(row[0])} if row else {"status": "error"}

app.mount("/", StaticFiles(directory="docs", html=True), name="docs")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)