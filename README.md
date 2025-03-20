— My bot template, uses **Aiogram** + **PostgreSQL** + **Aiogram-Dialog** for **simplified** and **convenient** work with widgets.
**FastApi + Uvicorn** (Webhooks for the bot, instead of aiohttp).
Convenient and fast deployment via **Docker**.

Several implementations that I liked I took from the template [wakaree](https://github.com/wakaree/aiogram_bot_template).

### ⬇️ Installation (Docker)
1. Clone the repository:
   1. `git clone https://github.com/kesevone/aiogram-dialog-bot-template`
   2. `cd aiogram-dialog-bot-template`
2. Set the variables
   1. `cp .env.example .env`
   2. In this file (`.env`), set all necessary values (_data from PostgreSQL, bot token, etc._)
3. Build and Run with Docker Compose: `docker compose up --build`

### 📂 Used technologies:
+ [Aiogram 3.19.0](https://github.com/aiogram/aiogram) (Telegram Bot Framework)
+ [Aiogram Dialog 2.3.1](https://github.com/Tishka17/aiogram_dialog) (convenient and simple development of menus and messages in the bot, as if it were a GUI application)
+ [Sulguk 0.8.0](https://github.com/Tishka17/sulguk) (HTML converter to Telegram entities)
+ [FastAPI Server](https://github.com/4u-org/aiogram_fastapi_server) (replacement of aiohttp for bot webhooks, since aiohttp is not intended for High-Level development of server options)
+ [PostgreSQL](https://www.postgresql.org/) (Database, best choice)
+ [SQLAlchemy 2.0.39](https://github.com/sqlalchemy/sqlalchemy) (Toolkit and ORM for working with a database)
+ [Alembic](https://github.com/alembic/alembic) (Lightweight database migration tool)
+ [Redis 5.2.1](https://github.com/redis/redis) (In-memory data storage for FSM and caching)

## 📌 TODO
+ [x] Integration APScheduler, a full-fledged task scheduler (.. broker).
+ [ ] Implementation of a web interface for managing the bot.
  + [ ] A full-fledged bot interface constructor (Dialogs auto-gen).
