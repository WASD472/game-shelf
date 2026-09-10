import os
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.environ.get("DATABASE_URL")

# Создаём таблицы при старте
def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id BIGINT PRIMARY KEY,
            username TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id SERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(id),
            title TEXT,
            status TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

init_db()

class Game(BaseModel):
    title: str
    status: str
    user_id: int

class User(BaseModel):
    user_id: int
    username: str

@app.post("/games/")
def add_game(game: Game):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO games (user_id, title, status) VALUES (%s, %s, %s)",
        (game.user_id, game.title, game.status)
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"message": f"Игра '{game.title}' добавлена"}

@app.get("/games/")
def get_games():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT games.id, users.username, games.title, games.status, games.date
        FROM games JOIN users ON games.user_id = users.id
    """)
    games = cur.fetchall()
    cur.close()
    conn.close()
    return games

@app.get("/games/view/{user_id}", response_class=HTMLResponse)
def view_user_games(user_id: int):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
        SELECT users.username, games.title, games.status, games.date
        FROM games JOIN users ON games.user_id = users.id
        WHERE users.id = %s
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        return "<h1 style='text-align:center;'>У этого пользователя нет игр</h1>"

    html = f"<h1 style='text-align:center;'>Игры пользователя {rows[0][0]}</h1><ul>"
    for row in rows:
        html += f"<li>{row[1]} — {row[2]} ({row[3]})</li>"
    html += "</ul>"
    return html

@app.post("/users/")
def add_user(user: User):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE id = %s", (user.user_id,))
    existing = cur.fetchone()
    if not existing:
        cur.execute("INSERT INTO users (id, username) VALUES (%s, %s)", (user.user_id, user.username))
        conn.commit()
    cur.close()
    conn.close()
    return {"message": "Пользователь сохранён"}

@app.get("/games/user/{user_id}")
def get_user_games(user_id: int):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT games.id, users.username, games.title, games.status, games.date
        FROM games JOIN users ON games.user_id = users.id
        WHERE users.id = %s
    """, (user_id,))
    games = cur.fetchall()
    cur.close()
    conn.close()
    return games

@app.delete("/games/{game_id}")
def delete_game(game_id: int):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("DELETE FROM games WHERE id = %s", (game_id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": f"Игра с id {game_id} удалена"}

@app.get("/health")
def health():
    return {"status": "ok"}