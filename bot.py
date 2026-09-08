import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN ="ВСТАВЬ_СВОЙ_ТОКЕН"
API_URL = "http://127.0.0.1:8000"

#Так это старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
                "Привет! Я бот для учёта игр.\n\n"
        "*Команды:*\n"
        "/start — список команд\n"
        "/games — показать все игры\n"
        "/delete — показать список для удаления\n"
        "/delete id — удалить игру с id \n\n"
        "*Как добавить игру:*\n"
        "прошел Название игры\n"
        "играю в Название игры",
        parse_mode="Markdown"
    )

#Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()#Чтобы пользователь мог писать как угодно

    if text.startswith("прошел"):#Если сообщение начинается с "прошел", то условие сработает.
        title = update.message.text[7:].strip()#Берёт текст сообщения, отрезает первые 7 символов и убирает лишние пробелы.Например - "прошел Ведьмак 3", а станет - "Ведьмак 3"     
        status = "Пройдено"
    elif text.startswith("играю в"):
        title = update.message.text[8:].strip()
        status = "Играю"
    else:
        await update.message.reply_text("Напиши 'прошел Название' или 'играю в Название.'")
        return

    if not title:
        await update.message.reply_text("Ты не указал название игры.")
        return


    try:#Обработка ошибок - try = попробуй выполнить код
        response = requests.post(#Отправляем POST-запрос на твой API.
            f"{API_URL}/games/",
            json={"title": title, "status": status}# данные, которые отправляем (название игры и статус)
        )
        if response.status_code == 200:#Код ответа от сервера. 200 - все хорошо. 400 - не найдено. 500 - ошибка
            await update.message.reply_text(f"Сохранил: {title} ({status})")
        else:
            await update.message.reply_text("Ошибка при сохранении.")
    except:# если что-то пошло не так и не смогли подключиться к серверу, выполни запасной вариант
        await update.message.reply_text("Не удалось подключиться к серверу")

async def cmd_games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(f"{API_URL}/games/")
        games = response.json()

        if not games:
            await update.message.reply_text("Список игр пуст.")
            return

        text = "*Мои игры:*\n\n"
        for i, game in enumerate(games, 1):
            text += f"{i}. {game['title']} — {game['status']} ({game['date']})\n"

        await update.message.reply_text(text, parse_mode="Markdown")#Markdown — чтобы звёздочки превратились в жирный шрифт
    except:
        await update.message.reply_text("Не удалось получить список.")


async def cmd_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        parts = update.message.text.split()

        if len(parts) == 1:#Если длина 1(просто delete, а не delete 2)
            # Пользователь написал просто /delete — показываем список
            response = requests.get(f"{API_URL}/games/")
            games = response.json()

            if not games:
                await update.message.reply_text("Список игр пуст.")
                return

            text = "*Выбери игру для удаления:*\n\n"
            for i, game in enumerate(games, 1):
                text += f"{i}. {game['title']} — {game['status']}\n"
            text += "\nНапиши: /delete НОМЕР"

            await update.message.reply_text(text, parse_mode="Markdown")
        else:
            # Удаляем по номеру
            response = requests.get(f"{API_URL}/games/")
            games = response.json()
            game_number = int(parts[1])#Это номер в списке, который видит пользователь.
            game = games[game_number - 1]#Список всех игр баз = Если пользователь написал 2, берём элемент с индексом 1:
            game_id = game["id"]

            response = requests.delete(f"{API_URL}/games/{game_id}")

            if response.status_code == 200:
                await update.message.reply_text(f"Игра '{game['title']}' удалена")
            else:
                await update.message.reply_text("Не удалось удалить игру")

    except:
        await update.message.reply_text("Напиши: /delete или /delete НОМЕР")
        


def main():
    app = Application.builder().token(TOKEN).build()#Создаём объект приложения Telegram-бота.Application.конструктор.подключаем_токен.собираем_предложение.app - это бот
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("games", cmd_games))
    app.add_handler(CommandHandler("delete", cmd_delete))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))#Регистрируем обработчик обычных сообщений.Текстовые,командные сообщения и обработчик сообщений
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()


  


