import logging

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from app.config import BOT_TOKEN
from app.logging_setup import setup_logging
from app.db.pool import init_pool
from app.db.schema import ensure_schema
from app.handlers.start import start
from app.handlers.add import quick_add
from app.handlers.report import week, month

logger = logging.getLogger("finance_bot")


async def on_startup(app: Application) -> None:
    pool = await init_pool()
    async with pool.acquire() as conn:
        await ensure_schema(conn)
    logger.info("DB schema ensured")


def build_app() -> Application:
    return (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(on_startup)   # ← ВАЖНО
        .build()
    )


def main() -> None:
    setup_logging()

    app = build_app()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("week", week))
    app.add_handler(CommandHandler("month", month))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, quick_add))

    logger.info("Bot started")
    app.run_polling()


if __name__ == "__main__":
    main()
