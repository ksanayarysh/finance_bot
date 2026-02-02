# Finance Bot (Telegram + Railway Postgres)

A minimal Telegram bot for personal finance tracking:
- Quick add: `еда 45.90 кофе` or `+зарплата 3500 аванс`
- Reports: `/week`, `/month`
- Data stored in Postgres (Railway)

## Local run (Windows / PowerShell)
```powershell
cd finance_bot
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

copy .env.example .env
notepad .env  # set BOT_TOKEN and DATABASE_URL (Railway)

python -m app.main
```

## Railway
Set Variables:
- `BOT_TOKEN`
- `DATABASE_URL` (from Railway Postgres)

Start command:
- `python -m app.main`
