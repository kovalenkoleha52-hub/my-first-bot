import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from duckduckgo_search import DDGS

# Токен берется из настроек Render
TG_TOKEN = os.getenv("TG_TOKEN")
bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Бот запущен и готов к работе! Спрашивай что угодно.")

@dp.message(F.text)
async def handle_text(message: types.Message):
    print(f"Запрос от {message.from_user.id}: {message.text}")
    try:
        with DDGS() as ddgs:
            # Исправленный вызов для версии 8.1.1
            results = ddgs.chat(message.text, model='gpt-4o-mini')
response = "".join([str(r) for r in results])
            await message.reply(response)
    except Exception as e:
        print(f"ОШИБКА: {e}")
        await message.answer("ИИ взял паузу. Попробуй еще раз через минуту.")

async def main():
    print("--- ЗАПУСК ОБНОВЛЕННОЙ ВЕРСИИ ---")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())






