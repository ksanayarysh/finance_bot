# app/main.py (замени функцию run_migrations и импортни ensure_schema)

import asyncio
import logging

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from app.config import BOT_TOKEN
from app.logging_setup import setup_logging
from app.db.pool import init_pool
from app.db.schema import ensure_schema  # <-- добавь
from app.handlers.start import start
from app.handlers.add import quick_add
from app.handlers.report import week, month

logger = logging.getLogger("finance_bot")

async def run_migrations() -> None:
    pool = await init_pool()
    async with pool.acquire() as conn:
        await ensure_schema(conn)  # <-- теперь не зависит от файла

def build_app() -> Application:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("week", week))
    app.add_handler(CommandHandler("month", month))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, quick_add))
    return app

async def main() -> None:
    setup_logging()
    await run_migrations()
    application = build_app()
    logger.info("Bot started")
    await application.run_polling(close_loop=False)

if __name__ == "__main__":
    asyncio.run(main())
