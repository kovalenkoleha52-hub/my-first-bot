import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from duckduckgo_search import DDGS

TG_TOKEN = os.getenv("TG_TOKEN")
bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Бот включен! Я использую быстрый поиск ответов. Спрашивай!")

@dp.message(F.text)
async def handle_text(message: types.Message):
    print(f"Запрос: {message.text}")
    try:
        with DDGS() as ddgs:
            # Используем поиск мгновенных ответов (Instant Answers)
            # Это работает быстрее и не блокируется серверами
            results = ddgs.answers(message.text)
            if results:
                answer = results[0]['text']
            else:
                # Если мгновенного ответа нет, берем краткое описание из поиска
                search_gen = ddgs.text(message.text, max_results=1)
                answer = next(search_gen)['body']
            
            await message.reply(answer)
    except Exception as e:
        print(f"ОШИБКА: {e}")
        await message.answer("Пока не могу найти ответ. Попробуй перефразировать вопрос!")

async def main():
    print("--- ЗАПУСК СВЕРХСТАБИЛЬНОЙ ВЕРСИИ ---")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())








