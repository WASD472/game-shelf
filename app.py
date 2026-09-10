import os
import threading
import uvicorn
from main import app

from bot import main as run_bot

@app.get("/health")
def health():
    return {"status": "ok"}

def start_bot():
    run_bot()

# Запускаем бота в отдельном потоке
bot_thread = threading.Thread(target=start_bot, daemon=True)
bot_thread.start()

if __name__ == "__main__":
    # Render передает порт через переменную окружения PORT
    port = int(os.environ.get("PORT", 8000))
    # Запускаем API-сервер
    uvicorn.run(app, host="0.0.0.0", port=port)