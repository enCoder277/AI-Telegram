import asyncio
import ollama
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command

# логи
logging.basicConfig(level=logging.INFO)
bot = Bot(token="7006979792:AAHNy7t2e4UzTMl9febEW7vrDdkvfvzaIIQ") #скрыть ключ
dp = Dispatcher()


def query_ollama(prompt: str, model_name: str = "your_model_name") -> str:
    try:
        response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': prompt}])  #хуйня здесь, ollama pull llama-3.1:8b
        return response['message']['content']
    except Exception as e:
        logging.error(f"Ошибка при запросе к Ollama: {e}")
        return "Произошла ошибка при запросе к модели."


@dp.message(F.text)
async def handle_message(message: types.Message):
    user_text = message.text
    ollama_response = query_ollama(user_text, "llama-3.1:8b")
    await message.answer(ollama_response)



@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я модель искусственного интеллекта, давай поговорим!")





# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())