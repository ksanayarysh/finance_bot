import asyncpg
from app.config import DATABASE_URL

_pool: asyncpg.Pool | None = None

def _needs_ssl(url: str) -> bool:
    # If user already specified sslmode in URL, don't override.
    return "sslmode=" not in url.lower()

async def init_pool() -> asyncpg.Pool:
    global _pool
    if _pool is not None:
        return _pool

    url = DATABASE_URL
    connect_kwargs = {}
    if _needs_ssl(url):
        # Railway Postgres often works best with SSL enabled.
        connect_kwargs["ssl"] = True

    _pool = await asyncpg.create_pool(
        dsn=url,
        min_size=1,
        max_size=5,
        **connect_kwargs,
    )
    return _pool

async def close_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None
