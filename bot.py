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
    await message.answer("Бот запущен! Теперь я использую стабильный ИИ. Спрашивай!")

@dp.message(F.text)
async def handle_text(message: types.Message):
    print(f"Запрос от {message.from_user.id}: {message.text}")
    try:
        with DDGS() as ddgs:
            # Используем встроенный метод chat, который возвращает строку
            response = ddgs.chat(message.text, model='gpt-4o-mini')
            await message.reply(response)
    except Exception as e:
        print(f"ОШИБКА: {e}")
        await message.answer("Произошла ошибка. Попробуй еще раз через пару секунд.")

async def main():
    print("--- ЗАПУСК ИСПРАВЛЕННОГО БОТА ---")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())




