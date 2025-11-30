import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from handlers.start import router as start_router
from handlers.categories import router as categories_router
from handlers.review import router as review_router

import db
import admin_app  # импортирует FastAPI приложение

import uvicorn

# Logging
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "bot.log")

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s: %(message)s")

# Console handler
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

# File handler (rotating)
try:
    from logging.handlers import RotatingFileHandler
    fh = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
except Exception:
    logger.warning("Could not create file handler for logging.")

from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(start_router)
dp.include_router(categories_router)
dp.include_router(review_router)

async def start_web():
    port = int(os.getenv("PORT", "8000"))
    config = uvicorn.Config("admin_app:app", host="0.0.0.0", port=port, loop="asyncio", log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    # init DB
    await db.init_db()
    # запустим веб сервер и polling параллельно
    web_task = asyncio.create_task(start_web())
    try:
        await dp.start_polling(bot)
    finally:
        web_task.cancel()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
