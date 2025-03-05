import asyncio
import ollama
import logging
from decouple import config
from elevenlabs import save
from elevenlabs.client import ElevenLabs
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.command import Command


# логи
logging.basicConfig(level=logging.INFO)
BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

ELEVENLABS_KEY = config('ELEVENLABS_TOKEN')
client = ElevenLabs(api_key=ELEVENLABS_KEY)

user_choice_voice_or_text = True

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    description = (
        "✨ Привет! Я твой виртуальный помощник, созданный на основе искусственного интеллекта! ✨\n\n"
        "💬 Готов ответить на твои вопросы, поддержать разговор или просто стать собеседником.\n"
        "🤖 Использую передовые технологии, чтобы помочь тебе находить решения, делиться знаниями и просто "
        "делать твой день чуточку интереснее!\n\n"
        "Давай поговорим! В каком формате ты бы хотел получать ответы? 😊"
    )
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Голосовые сообщения 🎙️", callback_data="set_audio_mode")],
            [InlineKeyboardButton(text="Текстовые сообщения 📝", callback_data="set_text_mode")]
        ]
    )
    await message.answer(description, reply_markup=kb)


@dp.message(Command("settings"))
async def cmd_settings(message: types.Message):
    current_mode = "Голосовые сообщения 🎙️" if user_choice_voice_or_text else "Текстовые сообщения 📝"

    settings_description = (
        f"⚙️ **Настройки режима**\n\n"
        f"Текущий режим: {current_mode}\n\n"
        f"Вы можете изменить режим с помощью кнопок ниже."
    )
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Текстовые сообщения 📝", callback_data="set_text_mode")],
            [InlineKeyboardButton(text="Голосовые сообщения 🎙️", callback_data="set_audio_mode")],
        ]
    )
    await message.answer(settings_description, reply_markup=kb, parse_mode="Markdown")


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "🛠 **Помощь**\n\n"
        "Я бот, использующий модель искусственного интеллекта.\n"
        "Вы можете задать мне любой вопрос или просто поговорить. 😊\n\n"
        "Вот список доступных команд:\n"
        "- `/start`: Запустить бота и начать с приветствия\n"
        "- `/help`: Показать это сообщение помощи\n"
        "- `/settings`: Настроить режим работы бота: текст или аудио\n\n"
        "💡 Вы также можете просто написать сообщение, и бот постарается ответить на ваш запрос."
    )
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="/start", callback_data="call_cmd_start")],
            [InlineKeyboardButton(text="/settings", callback_data="call_cmd_settings")],
            [InlineKeyboardButton(text="/help", callback_data="call_cmd_help")],
        ]
    )
    await message.answer(help_text, parse_mode="Markdown", reply_markup=kb)


def text_response_ollama(prompt: str, model_name: str = "your_model_name") -> str:
    try:
        response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content']
    except Exception as e:
        logging.error(f"Ошибка при запросе к Ollama: {e}")
        return "Произошла ошибка при запросе к модели."


ollama_voices = client.voices.get_all() #for optimization
def audio_response_ollama(prompt: str, model_name: str = "your_model_name"):
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
    user_text = message.text

    if user_choice_voice_or_text == True:
        ollama_response = audio_response_ollama(user_text, "llama3.1:latest")
        audio_file = FSInputFile(ollama_response, filename='EXAMPLE')
        await message.answer_audio(audio=audio_file)
    if user_choice_voice_or_text == False:
        ollama_response = text_response_ollama(user_text, "llama3.1:latest")
        await message.answer(ollama_response)


@dp.callback_query()
async def process_callback(callback_query: types.CallbackQuery):
    global user_choice_voice_or_text
    if callback_query.data == "set_audio_mode":
        user_choice_voice_or_text = True
        await callback_query.message.answer("Теперь бот будет отвечать голосовыми сообщениями! 🎙️")
    if callback_query.data == "set_text_mode":
        user_choice_voice_or_text = False
        await callback_query.message.answer("Теперь бот будет отвечать текстом! 📝")

    if callback_query.data == "call_cmd_start":
        await cmd_start(callback_query.message)
    if callback_query.data == "call_cmd_settings":
        await cmd_settings(callback_query.message)
    if callback_query.data == "call_cmd_help":
        await cmd_help(callback_query.message)

    # Уведомление Telegram о том, что запрос обработан
    await bot.answer_callback_query(callback_query.id)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())