import asyncio
import json
import os

import aiofiles
from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()
api_id = int(os.environ.get("api_id"))api_hash = os.environ.get("api_hash")


# Список чатов и ключевых слов
chats = ['ru_python', 'python_scripts', 'moscowpythonconf', 'rudepython', 'pythonchatru',
         'python_academy_chat', 'python_noobs', 'pythontalk_chat', 'pythonguruchat',
         'Python', 'pydjango', 'ChatPython', 'ru_python_beginners', 'karpovcourseschat']
words = ['pyrogram']


# Асинхронная функция для проверки наличия ключевых слов в сообщении
async def contains_keywords(message, keywords):
    if message:
        # Возвращает словарь, где ключи - это слова, а значения - True или False в зависимости от того, найдено ли слово в сообщении
        return {word: word in message.lower() for word in keywords}
    # Если сообщение отсутствует, возвращает словарь с False для всех слов
    return {word: False for word in keywords}

# Асинхронная функция для проверки сообщений
async def message_check(chat, message, semaphore):
    # Ожидание доступа к семафору
    async with semaphore:
        # Проверка сообщения на наличие ключевых слов
        keywords_found = await contains_keywords(message.text, words)
        # Если в сообщении найдено ключевое слово
        if message.text and any(keywords_found.values()):
            # Сбор данных о сообщении
            data = {
                "Чат": chat,
                "Найдена фраза": keywords_found,
                "Отправитель": f"@{message.from_user.username}" if message.from_user else "Неизвестно",
                "Дата отправки": str(message.date),
                "Сообщение полностью": message.text,
                "Ссылка на сообщение": f"https://t.me/{chat}/{message.id}",
            }
            # Возвращение ссылки на сообщение
            return data

# Асинхронная функция для проверки для проверки чатов
async def chat_check(app, chat, semaphore):
    print(f"Проверка чата: {chat}")
    # Получение истории сообщений из чата
    history = [message async for message in app.get_chat_history(chat, limit=1000)]
    chats_result = await asyncio.gather(*[message_check(chat, message, semaphore) for message in history])
    print(f"Всего обработано сообщений в чате '{chat}': {len(chats_result)}")
    result = [data for data in chats_result if data]
    return result


# Асинхронная функция для сохранения данных в формате JSON
async def save_to_file(data, filename='saved_messages.json'):
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    async with aiofiles.open(filename, 'w', encoding='utf-8') as f:
        # Запись данных в файл в формате JSON
        await f.write(json_data)
        print("Сообщения сохранены в файл")


# Основная асинхронная функция для работы со скриптом
async def main():
    all_data = []
    # Ограничение количества одновременных запросов, например, до 10
    semaphore = asyncio.Semaphore(10)

    # Инициализация асинхронного клиента Pyrogram
    async with Client("my_session", api_id=api_id, api_hash=api_hash) as app:
        # Проход по списку чатов
        chat_result = await asyncio.gather(*[chat_check(app, chat, semaphore) for chat in chats])

        # Сбор данных в один список. Убираем пустые списки
        [all_data.extend(lst) for lst in chat_result if lst]

        # Сохранение данных в файл
        await save_to_file(all_data)


asyncio.run(main())