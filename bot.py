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
    await message.answer("Бот готов! Спрашивай что угодно.")

@dp.message(F.text)
async def handle_text(message: types.Message):
    print(f"Запрос: {message.text}")
    try:
        # Используем упрощенный синхронный вызов, который стабильнее на Render
        with DDGS() as ddgs:
            # Модель claude-3-haiku работает быстрее и меньше блокируется
            response = ddgs.chat(message.text, model='claude-3-haiku')
            await message.reply(str(response))
    except Exception as e:
        print(f"ОШИБКА: {e}")
        await message.answer("ИИ сейчас перегружен. Попробуй через 10 секунд!")

async def main():
    print("--- ФИНАЛЬНЫЙ ЗАПУСК ---")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())









