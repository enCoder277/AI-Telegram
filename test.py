import asyncio
import ollama
import logging
from decouple import config
from elevenlabs import save
from elevenlabs.client import ElevenLabs
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import FSInputFile, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.command import Command

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

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
            [InlineKeyboardButton(text="ТЕКСТ", callback_data="command_text")],
            [InlineKeyboardButton(text="АУДИО", callback_data="command_audio")]
        ]
    )
    await message.answer(description, reply_markup=kb)

@dp.callback_query()
async def process_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "command_text":
        await text_example(callback_query.message)

    # Уведомление Telegram о том, что запрос обработан
    await bot.answer_callback_query(callback_query.id)



@dp.message(Command("text"))
async def text_example(message: types.Message):
    await message.answer("тест прошел успешно")





async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())