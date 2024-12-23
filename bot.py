import asyncio
import ollama
import logging
from decouple import config
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command

# логи
logging.basicConfig(level=logging.INFO)
BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))#закинуть decouple в requirements
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я модель искусственного интеллекта, давай поговорим!")

def query_ollama(prompt: str, model_name: str = "your_model_name") -> str:
    try:
        response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content']
    except Exception as e:
        logging.error(f"Ошибка при запросе к Ollama: {e}")
        return "Произошла ошибка при запросе к модели."


@dp.message(F.text)
async def handle_message(message: types.Message):
    user_text = message.text
    ollama_response = query_ollama(user_text, "llama3.1:latest")
    await message.answer(ollama_response)





# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())