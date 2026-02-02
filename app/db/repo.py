from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
import asyncpg

@dataclass(frozen=True)
class User:
    id: int
    tg_user_id: int
    currency: str
    tz: str

async def get_or_create_user(conn: asyncpg.Connection, tg_user_id: int) -> User:
    row = await conn.fetchrow(
        '''
        insert into users (tg_user_id) values ($1)
        on conflict (tg_user_id) do update set tg_user_id = excluded.tg_user_id
        returning id, tg_user_id, currency, tz
        ''',
        tg_user_id,
    )
    return User(
        id=int(row["id"]),
        tg_user_id=int(row["tg_user_id"]),
        currency=str(row["currency"]),
        tz=str(row["tz"]),
    )

async def ensure_default_categories(conn: asyncpg.Connection, user_id: int) -> None:
    defaults_expense = ["еда", "транспорт", "дом", "здоровье", "развлечения", "другое"]
    defaults_income = ["зарплата", "фриланс", "подарок", "другое"]

    for name in defaults_expense:
        await conn.execute(
            '''
            insert into categories (user_id, name, kind)
            values ($1, $2, 'expense')
            on conflict (user_id, kind, name) do nothing
            ''',
            user_id, name
        )

    for name in defaults_income:
        await conn.execute(
            '''
            insert into categories (user_id, name, kind)
            values ($1, $2, 'income')
            on conflict (user_id, kind, name) do nothing
            ''',
            user_id, name
        )

async def get_category_id(conn: asyncpg.Connection, user_id: int, kind: str, name: str) -> int | None:
    row = await conn.fetchrow(
        '''
        select id from categories
        where user_id = $1 and kind = $2 and lower(name) = lower($3)
        ''',
        user_id, kind, name
    )
    return int(row["id"]) if row else None

async def upsert_category(conn: asyncpg.Connection, user_id: int, kind: str, name: str) -> int:
    row = await conn.fetchrow(
        '''
        insert into categories (user_id, name, kind)
        values ($1, $2, $3)
        on conflict (user_id, kind, name) do update set name = excluded.name
        returning id
        ''',
        user_id, name, kind
    )
    return int(row["id"])

async def add_tx(
    conn: asyncpg.Connection,
    user_id: int,
    kind: str,
    category_id: int | None,
    amount: Decimal,
    note: str | None,
    happened_at: date,
) -> int:
    row = await conn.fetchrow(
        '''
        insert into transactions (user_id, kind, category_id, amount, note, happened_at)
        values ($1, $2, $3, $4, $5, $6)
        returning id
        ''',
        user_id, kind, category_id, amount, note, happened_at
    )
    return int(row["id"])

async def sum_by_category(
    conn: asyncpg.Connection,
    user_id: int,
    kind: str,
    date_from: date,
    date_to: date,
) -> list[tuple[str, Decimal]]:
    rows = await conn.fetch(
        '''
        select coalesce(c.name, 'без категории') as category,
               sum(t.amount)::numeric(12,2) as total
        from transactions t
        left join categories c on c.id = t.category_id
        where t.user_id = $1
          and t.kind = $2
          and t.happened_at between $3 and $4
        group by 1
        order by total desc
        ''',
        user_id, kind, date_from, date_to
    )
    return [(str(r["category"]), Decimal(str(r["total"]))) for r in rows]

async def sum_total(
    conn: asyncpg.Connection,
    user_id: int,
    kind: str,
    date_from: date,
    date_to: date,
) -> Decimal:
    row = await conn.fetchrow(
        '''
        select coalesce(sum(amount), 0)::numeric(12,2) as total
        from transactions
        where user_id = $1 and kind = $2 and happened_at between $3 and $4
        ''',
        user_id, kind, date_from, date_to
    )
    return Decimal(str(row["total"]))
