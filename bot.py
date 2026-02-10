import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from duckduckgo_search import DDGS

# Берем токен из переменных окружения
TG_TOKEN = os.getenv("TG_TOKEN")
bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Бот запущен в режиме сверхстабильного поиска! Спрашивай что угодно.")

@dp.message(F.text)
async def handle_text(message: types.Message):
    print(f"Запрос от {message.from_user.id}: {message.text}")
    try:
        with DDGS() as ddgs:
            # Используем расширенные параметры для обхода блокировок
            search_gen = ddgs.text(
                message.text, 
                region='ru-ru', 
                safesearch='off', 
                timelimit='y', 
                max_results=1
            )
            
            # Извлекаем результат
            res_list = list(search_gen)
            if res_list:
                answer = res_list[0]['body']
                await message.reply(answer)
            else:
                await message.answer("К сожалению, по этому запросу ничего не нашлось.")
                
    except Exception as e:
        print(f"ОШИБКА: {e}")
        await message.answer("Сервер поиска временно недоступен. Попробуй через пару минут!")

async def main():
    print("--- ЗАПУСК ФИНАЛЬНОЙ ВЕРСИИ ---")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())









