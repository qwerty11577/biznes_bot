from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

router = Router()

def main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💰 Доход"), KeyboardButton(text="💸 Расход")],
            [KeyboardButton(text="👥 Долги"), KeyboardButton(text="📦 Товары")],
            [KeyboardButton(text="📊 Отчёт"), KeyboardButton(text="📥 Excel отчёт")],
        ],
        resize_keyboard=True
    )
    return keyboard

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Этот бот поможет вам управлять вашим бизнесом.\n\n"
        "Выберите один из разделов:",
        reply_markup=main_menu()
    )