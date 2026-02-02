from telegram import Update
from telegram.ext import ContextTypes
from app.db.pool import init_pool
from app.db import repo

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    if not msg or not update.effective_user:
        return

    pool = await init_pool()
    async with pool.acquire() as conn:
        user = await repo.get_or_create_user(conn, update.effective_user.id)
        await repo.ensure_default_categories(conn, user.id)

    await msg.reply_text(
        "Привет. Я бот для учёта денег.\n\n"
        "Быстрый ввод:\n"
        "• `еда 45.90 кофе`\n"
        "• `+зарплата 3500 аванс`\n\n"
        "Команды:\n"
        "• /week — итоги за неделю\n"
        "• /month — итоги за месяц",
        parse_mode="Markdown",
    )
