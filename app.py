import os
import threading
import uvicorn
from main import app
from bot import main as run_bot

@app.get("/health")
def health():
    return {"status": "ok"}

def start_api():
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    # API в отдельном потоке
    api_thread = threading.Thread(target=start_api, daemon=True)
    api_thread.start()

    # Бот в главном потоке
    run_bot()