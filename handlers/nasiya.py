from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import database as db

router = Router()

class NasiyaState(StatesGroup):
    type_ = State()
    person = State()
    amount = State()
    description = State()

def nasiya_type_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔴 Мне должны"), KeyboardButton(text="🟢 Я должен")],
            [KeyboardButton(text="❌ Отмена")]
        ],
        resize_keyboard=True
    )

def cancel_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Отмена")]],
        resize_keyboard=True
    )

@router.message(F.text == "👥 Долги")
async def nasiya_start(message: Message, state: FSMContext):
    await state.set_state(NasiyaState.type_)
    await message.answer("👥 Выберите тип долга:", reply_markup=nasiya_type_keyboard())

@router.message(NasiyaState.type_)
async def nasiya_type(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        from handlers.start import main_menu
        await message.answer("Отменено.", reply_markup=main_menu())
        return
    if message.text not in ["🔴 Мне должны", "🟢 Я должен"]:
        await message.answer("Пожалуйста, выберите из кнопок!")
        return
    type_ = "menga" if message.text == "🔴 Мне должны" else "mendан"
    await state.update_data(type_=type_)
    await state.set_state(NasiyaState.person)
    await message.answer("👤 Введите имя человека:", reply_markup=cancel_keyboard())

@router.message(NasiyaState.person)
async def nasiya_person(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        from handlers.start import main_menu
        await message.answer("Отменено.", reply_markup=main_menu())
        return
    await state.update_data(person=message.text)
    await state.set_state(NasiyaState.amount)
    await message.answer("💰 Введите сумму:")

@router.message(NasiyaState.amount)
async def nasiya_amount(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        from handlers.start import main_menu
        await message.answer("Отменено.", reply_markup=main_menu())
        return
    try:
        amount = float(message.text.replace(",", "."))
        await state.update_data(amount=amount)
        await state.set_state(NasiyaState.description)
        await message.answer("📝 Введите описание (или напишите -):")
    except ValueError:
        await message.answer("❗ Введите число. Например: 500000")

@router.message(NasiyaState.description)
async def nasiya_description(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        from handlers.start import main_menu
        await message.answer("Отменено.", reply_markup=main_menu())
        return
    data = await state.get_data()
    await db.add_debt(message.from_user.id, data["person"], data["amount"], data["type_"], message.text)
    await state.clear()
    from handlers.start import main_menu
    type_text = "Мне должны" if data["type_"] == "menga" else "Я должен"
    await message.answer(
        f"✅ Долг записан!\n\n"
        f"👤 Человек: {data['person']}\n"
        f"💰 Сумма: {data['amount']:,.0f} сум\n"
        f"📋 Тип: {type_text}\n"
        f"📝 Описание: {message.text}",
        reply_markup=main_menu()
    )

@router.message(F.text == "📋 Список долгов")
async def nasiya_list(message: Message):
    debts = await db.get_debts(message.from_user.id)
    if not debts:
        from handlers.start import main_menu
        await message.answer("📭 Долгов нет!", reply_markup=main_menu())
        return
    text = "👥 Список долгов:\n\n"
    for debt in debts:
        id_, person, amount, type_, desc = debt
        emoji = "🔴" if type_ == "menga" else "🟢"
        type_text = "мне должны" if type_ == "menga" else "я должен"
        text += f"{emoji} {person} — {amount:,.0f} сум ({type_text})\n📝 {desc}\n/tolov_{id_}\n\n"
    from handlers.start import main_menu
    await message.answer(text, reply_markup=main_menu())