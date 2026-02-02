from __future__ import annotations
from datetime import date, timedelta

def week_range(d: date) -> tuple[date, date]:
    # Monday..Sunday
    start = d - timedelta(days=d.weekday())
    end = start + timedelta(days=6)
    return start, end

def month_range(d: date) -> tuple[date, date]:
    start = d.replace(day=1)
    if start.month == 12:
        next_month = start.replace(year=start.year + 1, month=1, day=1)
    else:
        next_month = start.replace(month=start.month + 1, day=1)
    end = next_month - timedelta(days=1)
    return start, end
