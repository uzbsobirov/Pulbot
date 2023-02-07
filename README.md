# Aiogram Money Bot
This is a simple money bot using aiogram and PostgreSQL as database
```
⚠️ Make sure you have a Postgresql database installed
```
1. Rename `.env_example` to `.env`
2. Create virtualenv:
```
$ python -m venv venv
```
3. Install requirements using: 
```
$ pip install -r requirements.txt
```
4. Configurate .env
```
ADMINS=your_telegram_id
BOT_TOKEN=your_bot_token

DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=your_db_name
```
6. And run the bot
```
$ python app.py
```

7. Add your logic to own bot, it's up to you!
