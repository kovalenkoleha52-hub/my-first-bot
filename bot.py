import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from duckduckgo_search import AsyncDDGS
import os

# Берем только токен Телеграм
TG_TOKEN = os.getenv("TG_TOKEN")

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Бот переключен на резервный ИИ! Пиши любой вопрос.")

@dp.message(F.text)
async def handle_text(message: types.Message):
    print(f"Запрос от {message.from_user.id}: {message.text}")
    try:
        # Используем бесплатный ИИ через DuckDuckGo
        async with AsyncDDGS() as ddgs:
            results = await ddgs.chat(message.text, model='gpt-4o-mini')
            await message.reply(results)
    except Exception as e:
        print(f"ОШИБКА: {e}")
        await message.answer("Даже резервный ИИ приуныл. Попробуй позже.")

async def main():
    print("--- ЗАПУСК РЕЗЕРВНОГО БОТА ---")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


