from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

@dataclass(frozen=True)
class ParsedInput:
    kind: str            # 'expense'|'income'
    category: str
    amount: Decimal
    note: str | None

def parse_quick_input(text: str) -> ParsedInput | None:
    t = text.strip()
    if not t:
        return None

    kind = "expense"
    if t.startswith("+"):
        kind = "income"
        t = t[1:].strip()
    elif t.startswith("-"):
        kind = "expense"
        t = t[1:].strip()

    parts = t.split()
    if len(parts) < 2:
        return None

    category = parts[0].strip().lower()
    raw_amount = parts[1].replace(",", ".")
    try:
        amount = Decimal(raw_amount).quantize(Decimal("0.01"))
    except InvalidOperation:
        return None

    note = " ".join(parts[2:]).strip() or None
    return ParsedInput(kind=kind, category=category, amount=amount, note=note)
