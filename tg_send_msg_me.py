import asyncio
import os

from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()
api_id = int(os.environ.get("api_id"))
api_hash = os.environ.get("api_hash")


async def main():
    app = Client("session_name4", api_id=api_id, api_hash=api_hash)
    async with app:
        await app.send_message("@aerohcss", "Message sent with **Pyrogram**!")
asyncio.run(main())