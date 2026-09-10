# Игровая полка

Fullstack-проект для учёта игр.(С кривым пока что frontend )

## Что внутри

- Telegram-бот
- API на FastAPI
- Проект использует PostgreSQL (Aiven)
- Веб-страница для просмотра игр

## Возможности

- Добавление игр через бота
- У каждого пользователя свой список
- Просмотр игр через бота или сайт
- Удаление игр

## Как запустить

1. Установить зависимости:

pip install -r requirements.txt

2. Запустить API:

uvicorn main:app --reload

3. Создать файл .env с переменными:

TELEGRAM_BOT_TOKEN=твой_токен
API_URL=http://127.0.0.1:8000
DATABASE_URL=твоя_строка_подключения

4. Запустить бота:

python bot.py

5. Открыть сайт: https://game-shelf67.netlify.app

## Команды бота

/start — Приветствие и список команд
/games — мои игры
/delete — список для удаления
/delete 2 — удалить игру под номером

## Добавление игры

прошел Название игры
играю в Название игры

## API маршруты

- POST /users/ — создать пользователя
- POST /games/ — добавить игру
- GET /games/ — все игры
- GET /games/user/{user_id} — игры пользователя
- GET /games/view/{user_id} — HTML-страница
- DELETE /games/{game_id} — удалить игру

## Как узнать свой Telegram id

Напишите боту @userinfobot — он покажет ваш id.

## Деплой

Проект развёрнут на Render (бесплатный тариф).

## Переменные окружения

Для работы нужны:

- TELEGRAM_BOT_TOKEN — токен бота
- API_URL — адрес API
- DATABASE_URL — строка подключения к PostgreSQL

## Где взять DATABASE_URL

1. Зарегистрируйся на aiven.io
2. Создай PostgreSQL (план Free)
3. Скопируй Service URI — это и есть DATABASE_URL

## Где взять API_URL

API_URL — это публичный адрес твоего сервиса на Render.

Например: https://game-shelf-bot.onrender.com

Он появляется после создания Web Service на render.com.

## Ссылки

- Сайт: https://game-shelf67.netlify.app
- API: https://game-shelf-bot.onrender.com