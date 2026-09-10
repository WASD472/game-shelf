import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")


#Достаем пользователя из Telegram и берм его id и имя
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    username = user.username or user.first_name or "Пользователь"

    # Сохраняем пользователя
    try:
        requests.post(f"{API_URL}/users/", json={"user_id": user_id, "username": username})
    except:
        pass

    await update.message.reply_text(
        "Привет! Я бот для учёта игр.\n\n"
        "Команды:\n"
        "/games — мои игры\n"
        "/delete — удалить игру\n\n"
        "/site — ссылка на твою страницу\n"
        "Добавить:\n"
        "прошел Название игры\n"
        "играю в Название игры"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user_id = update.effective_user.id

    if text.startswith("прошел"):
        title = update.message.text[7:].strip()
        status = "Пройдено"
    elif text.startswith("играю в"):
        title = update.message.text[8:].strip()
        status = "Играю"
    else:
        await update.message.reply_text("Напиши 'прошел Название' или 'играю в Название'")
        return

    if not title:
        await update.message.reply_text("Укажи название игры")
        return

    try:
        response = requests.post(
            f"{API_URL}/games/",
            json={"user_id": user_id, "title": title, "status": status}
        )
        if response.status_code == 200:
            await update.message.reply_text(f"Сохранил: {title} ({status})")
        else:
            await update.message.reply_text("Ошибка при сохранении")
    except:
        await update.message.reply_text("Не удалось подключиться к серверу")

async def cmd_games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        response = requests.get(f"{API_URL}/games/user/{user_id}")
        games = response.json()

        if not games:
            await update.message.reply_text("У тебя пока нет игр.")
            return

        text = "Мои игры:\n\n"
        for i, game in enumerate(games, 1):
            text += f"{i}. {game['title']} — {game['status']} ({game['date']})\n"

        await update.message.reply_text(text)
    except:
        await update.message.reply_text("Не удалось получить список")


async def cmd_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    parts = update.message.text.split()

    if len(parts) == 1:
        try:
            response = requests.get(f"{API_URL}/games/user/{user_id}")
            games = response.json()

            if not games:
                await update.message.reply_text("У тебя пока нет игр.")
                return

            text = "Выбери игру для удаления:\n\n"
            for i, game in enumerate(games, 1):
                text += f"{i}. {game['title']} — {game['status']}\n"
            text += "\nНапиши: /delete НОМЕР"

            await update.message.reply_text(text)
        except:
            await update.message.reply_text("Не удалось получить список")
    else:
        try:
            response = requests.get(f"{API_URL}/games/user/{user_id}")
            games = response.json()
            game = games[int(parts[1]) - 1]
            real_id = game["id"]

            response = requests.delete(f"{API_URL}/games/{real_id}")
            if response.status_code == 200:
                await update.message.reply_text(f"Игра '{game['title']}' удалена")
            else:
                await update.message.reply_text("Не удалось удалить игру")
        except:
            await update.message.reply_text("Неверный номер")

async def cmd_site(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    url = f"https://game-shelf67.netlify.app/?user={user_id}"
    await update.message.reply_text(f"Твоя страница с играми:\n{url}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("games", cmd_games))
    app.add_handler(CommandHandler("delete", cmd_delete))
    app.add_handler(CommandHandler("site", cmd_site))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()


  


