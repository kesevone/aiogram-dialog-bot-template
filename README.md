— My bot template, uses **Aiogram** + **PostgreSQL** + **Aiogram-Dialog** for **simplified** and **convenient** work with widgets.
**FastApi + Uvicorn** (Webhooks for the bot, instead of aiohttp).
Several implementations that I liked I took from the template [wakaree](https://github.com/wakaree/aiogram_bot_template).

### ⬇️ Installation (Ubuntu/Linux/Windows)
**Before setting up the bot**, you need to prepare **PostgreSQL** (user and database itself) and **Redis**.
You can find links to the technologies used below.

1. Install the **virtual environment** with **Python >= 3.11** with the command: `python -m venv .venv`
2. Activate **virtual environment** with the command: `source .venv/bin/activate` or `.venv/Scripts/activate`
3. Install the necessary libraries with the command: `pip install -r requirements.txt`
4. Go to the `src` folder, find and change the file name `.env.dist` to `.env`
5. In this file, set all necessary values (data from PostgreSQL, bot token, etc.)
6. Run **migrations to create tables** in the database with the command: `alembic upgrade head`
7. Run the bot with the command: `python main.py`.

### 📂 Used technologies:
+ [Aiogram 3.7.0](https://github.com/aiogram/aiogram) (Telegram Bot Framework)
+ [Aiogram Dialog 2.1.0](https://github.com/Tishka17/aiogram_dialog) (convenient and simple development of menus and messages in the bot, as if it were a GUI application)
+ [Sulguk 0.8.0](https://github.com/Tishka17/sulguk) (HTML converter to Telegram entities)
+ [FastAPI Server](https://github.com/4u-org/aiogram_fastapi_server) (replacement of aiohttp for bot webhooks, since aiohttp is not intended for High-Level development of server options)
+ [PostgreSQL](https://www.postgresql.org/) (Database, best choice)
+ [SQLAlchemy 2.0.30](https://github.com/sqlalchemy/sqlalchemy) (Toolkit and ORM for working with a database)
+ [Alembic](https://github.com/alembic/alembic) (Lightweight database migration tool)
+ [Redis 5.0.6](https://github.com/redis/redis) (In-memory data storage for FSM and caching)

## 📌 TODO
+ [✅] Integration APScheduler, a full-fledged task scheduler (.. broker).
+ [ ] Dishka DI framework from Tishka17.
