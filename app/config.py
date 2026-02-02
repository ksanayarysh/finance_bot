import os
from dotenv import load_dotenv

# Loads .env locally. On Railway, variables come from the environment.
load_dotenv()

def env(name: str) -> str:
    val = os.getenv(name)
    if val is None or val.strip() == "":
        raise RuntimeError(f"Missing env var: {name}")
    return val

BOT_TOKEN = env("BOT_TOKEN")
DATABASE_URL = env("DATABASE_PUBLIC_URL")
