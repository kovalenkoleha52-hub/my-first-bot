import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from duckduckgo_search import AsyncDDGS

# Токен из настроек Render
TG_TOKEN = os.getenv("TG_TOKEN")
bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Бот запущен и готов! Спрашивай что угодно.")

@dp.message(F.text)
async def handle_text(message: types.Message):
    print(f"Запрос от {message.from_user.id}: {message.text}")
    try:
        # Используем асинхронную версию для Render
        async with AsyncDDGS() as ddgs:
            response = await ddgs.achat(message.text, model='gpt-4o-mini')
            await message.reply(response)
    except Exception as e:
        print(f"ОШИБКА ИИ: {e}")
        await message.answer("Связь нестабильна, попробуй еще раз через 10 секунд.")

async def main():
    print("--- ЗАПУСК АСИНХРОННОЙ ВЕРСИИ ---")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())








