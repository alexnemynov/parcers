import asyncio
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()
api_id = int(os.environ.get("api_id"))
api_hash = os.environ.get("api_hash")
chat_id = '@bbchat'

# Определение временного периода
end_time = datetime.now()
start_time = end_time - timedelta(hours=6)

async def main():
    # Создание клиента Pyrogram
    app = Client("my_session", api_id=api_id, api_hash=api_hash)
    async with app:
        # Получение истории чата начиная с start_time
        async for message in app.get_chat_history(chat_id, offset_date=end_time):
            # Проверка даты сообщения
            if message.date < start_time:
                break
            print(message.text)

# Запуск асинхронной функции
asyncio.run(main())