import os
import google.generativeai as genai
from dotenv import load_dotenv
# ... остальные импорты ...

load_dotenv() # Загружает данные из переменных окружения

# Вместо самих ключей пишем вот это:
TG_TOKEN = os.getenv("TG_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")# Настройка ИИ
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Память бота
chat_sessions = {}

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    chat_sessions[message.from_user.id] = model.start_chat(history=[])
    await message.answer("Бот готов! Пришли текст или фото.")

@dp.message(Command("draw"))
async def draw(message: types.Message):
    prompt = message.text.replace("/draw", "").strip()
    if not prompt: return await message.answer("Напиши что нарисовать после /draw")
    url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}"
    await message.reply_photo(photo=url, caption=f"Рисунок: {prompt}")

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    photo_bytes = await bot.download_file(file.file_path)
    try:
        img_data = [{"mime_type": "image/jpeg", "data": photo_bytes.read()}]
        response = model.generate_content(["Что тут?" ] + img_data)
        await message.reply(response.text)
    except Exception as e:
        await message.answer(f"Ошибка ИИ: {e}")

@dp.message(F.text)
async def handle_text(message: types.Message):
    # ЛОГ: Ты увидишь это в черном окне
    print(f"Сообщение от {message.from_user.id}: {message.text}")
    
    uid = message.from_user.id
    if uid not in chat_sessions:
        chat_sessions[uid] = model.start_chat(history=[])
    try:
        response = chat_sessions[uid].send_message(message.text)
        await message.reply(response.text)
    except Exception as e:
        await message.answer("Google не отвечает. Попробуй включить VPN на ПК.")

async def main():
    print("--- ЗАПУСК... ---")
    await dp.start_polling(bot)

if __name__ == "__main__":

    asyncio.run(main())
