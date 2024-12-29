"""
перевести на API llm
валидация при воде (message)
реализовать историю чата и память чата
реализовать выбор между текстом и гс
доделать help
вывод гс
"""

import asyncio
import ollama
import logging
from decouple import config
from elevenlabs import save
from elevenlabs.client import ElevenLabs
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import FSInputFile
from aiogram.filters.command import Command


# логи
logging.basicConfig(level=logging.INFO)
BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

ELEVENLABS_KEY = config('ELEVENLABS_TOKEN')
client = ElevenLabs(api_key=ELEVENLABS_KEY)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    description = (
        "✨ Привет! Я твой виртуальный помощник, созданный на основе искусственного интеллекта! ✨\n\n"
        "💬 Готов ответить на твои вопросы, поддержать разговор или просто стать собеседником.\n"
        "🤖 Использую передовые технологии, чтобы помочь тебе находить решения, делиться знаниями и просто "
        "делать твой день чуточку интереснее!\n\n"
        "Давай поговорим? 😊"
    )
    await message.answer(description)

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "🛠 Help:\n\n"
        "Я бот, использующий модель искусственного интеллекта. "
        "Вы можете задать мне любой вопрос или просто поговорить. 😊\n\n"
        "Попробуй написать что-нибудь, и я постараюсь тебе помочь!"
    )
    await message.answer(help_text)



def text_response_ollama(prompt: str, model_name: str = "your_model_name"):
    try:
        response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content']
    except Exception as e:
        logging.error(f"Ошибка при запросе к Ollama: {e}")
        return "Произошла ошибка при запросе к модели."

ollama_voices = client.voices.get_all() #for optimization
def audio_response_ollama(prompt: str, model_name: str = "your_model_name") -> str:
    try:
        text_response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': prompt}])
        audio_response = client.generate(text=text_response['message']['content'], voice=ollama_voices.voices[3])
        save(audio_response, 'audio_response.mp3')

        return 'audio_response.mp3'
    except Exception as e:
        logging.error(f"Ошибка при запросе к Ollama: {e}")
        return "Произошла ошибка при запросе к модели."




@dp.message(F.text)
async def handle_message(message: types.Message):
    USER_CHOICE = True # будет реализован выбор пользователем

    user_text = message.text

    if USER_CHOICE == True:
        ollama_response = audio_response_ollama(user_text, "llama3.1:latest")
        audio_file = FSInputFile(ollama_response, filename='EXAMPLE')
        await message.answer_audio(audio=audio_file)
        await message.answer_voice(audio=audio_file) #- передать сюда ссылку на файл (str) локального файла через InputFile.
    if USER_CHOICE == False:
        ollama_response = text_response_ollama(user_text, "llama3.1:latest")
        await message.answer(ollama_response)






# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())