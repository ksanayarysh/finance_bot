from datetime import date
from telegram import Update
from telegram.ext import ContextTypes
from app.db.pool import init_pool
from app.db import repo
from app.domain.dates import week_range, month_range
from app.services.summaries import build_report

async def week(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    tg_user = update.effective_user
    if not msg or not tg_user:
        return

    d1, d2 = week_range(date.today())

    pool = await init_pool()
    async with pool.acquire() as conn:
        user = await repo.get_or_create_user(conn, tg_user.id)
        text = await build_report(conn, user, d1, d2)

    await msg.reply_text(text)

async def month(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    tg_user = update.effective_user
    if not msg or not tg_user:
        return

    d1, d2 = month_range(date.today())

    pool = await init_pool()
    async with pool.acquire() as conn:
        user = await repo.get_or_create_user(conn, tg_user.id)
        text = await build_report(conn, user, d1, d2)

    await msg.reply_text(text)
