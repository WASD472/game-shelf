from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from fastapi.responses import HTMLResponse#Импорт нужен, чтобы браузер отображал красивую страницу, а не кусок текста с тегами.



app = FastAPI()

conn = sqlite3.connect("games.db")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS games(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
status TEXT,
date TEXT)
""")
conn.commit()
conn.close()

class Game(BaseModel):
    title: str
    status : str

@app.post("/games/")
def add_game(game: Game):
    conn = sqlite3.connect("games.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO games (title, status, date) VALUES (?, ?, datetime('now'))",
                (game.title, game.status)
    )
    conn.commit()
    conn.close()
    return {"message": f"Игра '{game.title}' добавлена." }

@app.get("/games/")
def get_games():
    conn = sqlite3.connect("games.db")
    cur = conn.cursor()
    cur.execute("SELECT id, title, status, date FROM games")
    rows = cur.fetchall()
    conn.close()

    games = []
    for row in rows:
        games.append({"id": row[0], "title": row[1], "status": row[2], "date": row[3]})
    return games


@app.get("/games/view/", response_class=HTMLResponse)
def view_games():
    conn = sqlite3.connect("games.db")
    cur = conn.cursor()
    cur.execute("SELECT id, title, status, date FROM games")
    rows = cur.fetchall()
    conn.close()

    html = "<h1 style='text-align:center;'>Список игр</h1>"

    if not rows:
        html += "<p style='text-align:center;'>Ты ничего не прошёл!</p>"
    else:
        html += "<table style='margin:0 auto; border-collapse:collapse;'>"
        html += "<tr><th style='padding:8px 20px;'>#</th><th style='padding:8px 20px;'>Игра</th><th style='padding:8px 20px;'>Статус</th><th style='padding:8px 20px;'>Дата</th></tr>"
        for i, row in enumerate(rows, 1):
            html += f"<tr><td style='padding:6px 20px; text-align:center;'>{i}</td><td style='padding:6px 20px;'>{row[1]}</td><td style='padding:6px 20px;'>{row[2]}</td><td style='padding:6px 20px;'>{row[3]}</td></tr>"
        html += "</table>"

    return html


@app.delete("/games/{game_id}")
def delete_game(game_id: int):#(id игры: подсказка что целое число)
    conn = sqlite3.connect("games.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM games WHERE id = ?", (game_id,))
    conn.commit()
    conn.close()
    return {"message": f"Игра с id {game_id} удалена."}
