"""Initialize the database schema."""

import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from backend.models.database import init_db


async def main():
    os.makedirs("./data/db", exist_ok=True)
    await init_db()
    print("Database initialized successfully.")


if __name__ == "__main__":
    asyncio.run(main())
