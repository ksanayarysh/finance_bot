from __future__ import annotations
from datetime import date
from decimal import Decimal
from app.db import repo

def fmt_money(x: Decimal, currency: str) -> str:
    return f"{x:.2f} {currency}"

async def build_report(conn, user: repo.User, date_from: date, date_to: date) -> str:
    exp_total = await repo.sum_total(conn, user.id, "expense", date_from, date_to)
    inc_total = await repo.sum_total(conn, user.id, "income", date_from, date_to)

    exp_by_cat = await repo.sum_by_category(conn, user.id, "expense", date_from, date_to)
    inc_by_cat = await repo.sum_by_category(conn, user.id, "income", date_from, date_to)

    lines: list[str] = []
    lines.append(f"📅 Период: {date_from.isoformat()} — {date_to.isoformat()}")
    lines.append("")
    lines.append(f"💸 Расходы: {fmt_money(exp_total, user.currency)}")
    for cat, total in exp_by_cat[:10]:
        lines.append(f"  • {cat}: {fmt_money(total, user.currency)}")

    lines.append("")
    lines.append(f"💰 Доходы: {fmt_money(inc_total, user.currency)}")
    for cat, total in inc_by_cat[:10]:
        lines.append(f"  • {cat}: {fmt_money(total, user.currency)}")

    balance = inc_total - exp_total
    lines.append("")
    lines.append(f"🧾 Баланс: {fmt_money(balance, user.currency)}")
    return "\n".join(lines)
