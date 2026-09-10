from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from fastapi.responses import HTMLResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],#разрешаем запросы с любых источников
    allow_methods=["*"],#любые методы (GET, POST, DELETE)
    allow_headers=["*"],#любые заголовки
)

# Создаём таблицы
conn = sqlite3.connect("games.db")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        status TEXT,
        date TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
""")

# Модель игры
class Game(BaseModel):
    title: str
    status: str
    user_id: int

class User(BaseModel):
    user_id: int
    username: str

# Добавить игру
@app.post("/games/")
def add_game(game: Game):
    conn = sqlite3.connect("games.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO games (user_id, title, status, date) VALUES (?, ?, ?, datetime('now'))",
        (game.user_id, game.title, game.status)
    )
    conn.commit()
    conn.close()
    return {"message": f"Игра '{game.title}' добавлена"}

# Все игры
@app.get("/games/")
def get_games():
    conn = sqlite3.connect("games.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT games.id, users.username, games.title, games.status, games.date
        FROM games
        JOIN users ON games.user_id = users.id 
    """)#JOIN users ON games.user_id = users.id - Присоединяем таблицу users, связывая по id 
    rows = cur.fetchall()
    conn.close()

    games = []
    for row in rows:
        games.append({
            "id": row[0],
            "username": row[1],
            "title": row[2],
            "status": row[3],
            "date": row[4]
        })
    return games

# Показывает игры только одного пользователя.
@app.get("/games/view/{user_id}", response_class=HTMLResponse)
def view_user_games(user_id: int):
    conn = sqlite3.connect("games.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT users.username, games.title, games.status, games.date
        FROM games
        JOIN users ON games.user_id = users.id
        WHERE users.id = ?
    """, (user_id,))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return "<h1 style='text-align:center;'>У этого пользователя нет игр</h1>"

    html = f"<h1 style='text-align:center;'>Игры пользователя {rows[0][0]}</h1><ul>"
    for row in rows:
        html += f"<li>{row[1]} — {row[2]} ({row[3]})</li>"
    html += "</ul>"
    return html


@app.post("/users/")#функция в API, которая сохраняет пользователя в базу
def add_user(user: User):
    conn = sqlite3.connect("games.db")
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE id = ?", (user.user_id,))
    existing = cur.fetchone()

    if not existing:
        cur.execute("INSERT INTO users (id, username) VALUES (?, ?)", (user.user_id, user.username))
        conn.commit()

    conn.close()
    return {"message": "Пользователь сохранён"}

@app.get("/games/user/{user_id}")#Отдаёт игры только одного пользователя.Чтобы каждый видел только своё, а не общий список.
def get_user_games(user_id: int):
    conn = sqlite3.connect("games.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT games.id, users.username, games.title, games.status, games.date
        FROM games
        JOIN users ON games.user_id = users.id
        WHERE users.id = ?
    """,(user_id,))
    rows = cur.fetchall()
    conn.close()

    games = []
    for row in rows:
        games.append({
            "id": row[0],
            "username": row[1],
            "title": row[2],
            "status": row[3],
            "date": row[4]
        })
    return games

@app.delete("/games/{game_id}")
def delete_game(game_id: int):
    conn = sqlite3.connect("games.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM games WHERE id = ?", (game_id,))
    conn.commit()
    conn.close()
    return {"message": f"Игра с id {game_id} удалена"}
