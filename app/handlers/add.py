from datetime import date
from telegram import Update
from telegram.ext import ContextTypes
from app.db.pool import init_pool
from app.db import repo
from app.domain.parsing import parse_quick_input

async def quick_add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    tg_user = update.effective_user
    if not msg or not tg_user or not msg.text:
        return

    parsed = parse_quick_input(msg.text)
    if not parsed:
        return  # ignore non-transaction messages

    pool = await init_pool()
    async with pool.acquire() as conn:
        user = await repo.get_or_create_user(conn, tg_user.id)

        cat_id = await repo.get_category_id(conn, user.id, parsed.kind, parsed.category)
        if cat_id is None:
            cat_id = await repo.upsert_category(conn, user.id, parsed.kind, parsed.category)

        tx_id = await repo.add_tx(
            conn=conn,
            user_id=user.id,
            kind=parsed.kind,
            category_id=cat_id,
            amount=parsed.amount,
            note=parsed.note,
            happened_at=date.today(),
        )

    sign = "💸" if parsed.kind == "expense" else "💰"
    note = f" ({parsed.note})" if parsed.note else ""
    await msg.reply_text(f"{sign} Записано: {parsed.category} {parsed.amount:.2f}{note}  [id {tx_id}]")
