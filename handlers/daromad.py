from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import database as db

router = Router()

class DaromadState(StatesGroup):
    amount = State()
    category = State()
    description = State()

class XarajatState(StatesGroup):
    amount = State()
    category = State()
    description = State()

def cancel_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Отмена")]],
        resize_keyboard=True
    )

@router.message(F.text == "💰 Доход")
async def daromad_start(message: Message, state: FSMContext):
    await state.set_state(DaromadState.amount)
    await message.answer("💰 Введите сумму дохода:", reply_markup=cancel_keyboard())

@router.message(DaromadState.amount)
async def daromad_amount(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        from handlers.start import main_menu
        await message.answer("Отменено.", reply_markup=main_menu())
        return
    try:
        amount = float(message.text.replace(",", "."))
        await state.update_data(amount=amount)
        await state.set_state(DaromadState.category)
        await message.answer("📂 Введите категорию (например: продажи, услуги):")
    except ValueError:
        await message.answer("❗ Введите число. Например: 500000")

@router.message(DaromadState.category)
async def daromad_category(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        from handlers.start import main_menu
        await message.answer("Отменено.", reply_markup=main_menu())
        return
    await state.update_data(category=message.text)
    await state.set_state(DaromadState.description)
    await message.answer("📝 Введите описание (или напишите -):")

@router.message(DaromadState.description)
async def daromad_description(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        from handlers.start import main_menu
        await message.answer("Отменено.", reply_markup=main_menu())
        return
    data = await state.get_data()
    await db.add_transaction(message.from_user.id, "daromad", data["amount"], data["category"], message.text)
    await state.clear()
    from handlers.start import main_menu
    await message.answer(
        f"✅ Доход записан!\n\n"
        f"💰 Сумма: {data['amount']:,.0f} сум\n"
        f"📂 Категория: {data['category']}\n"
        f"📝 Описание: {message.text}",
        reply_markup=main_menu()
    )

@router.message(F.text == "💸 Расход")
async def xarajat_start(message: Message, state: FSMContext):
    await state.set_state(XarajatState.amount)
    await message.answer("💸 Введите сумму расхода:", reply_markup=cancel_keyboard())

@router.message(XarajatState.amount)
async def xarajat_amount(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        from handlers.start import main_menu
        await message.answer("Отменено.", reply_markup=main_menu())
        return
    try:
        amount = float(message.text.replace(",", "."))
        await state.update_data(amount=amount)
        await state.set_state(XarajatState.category)
        await message.answer("📂 Введите категорию (например: аренда, зарплата):")
    except ValueError:
        await message.answer("❗ Введите число. Например: 200000")

@router.message(XarajatState.category)
async def xarajat_category(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        from handlers.start import main_menu
        await message.answer("Отменено.", reply_markup=main_menu())
        return
    await state.update_data(category=message.text)
    await state.set_state(XarajatState.description)
    await message.answer("📝 Введите описание (или напишите -):")

@router.message(XarajatState.description)
async def xarajat_description(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        from handlers.start import main_menu
        await message.answer("Отменено.", reply_markup=main_menu())
        return
    data = await state.get_data()
    await db.add_transaction(message.from_user.id, "xarajat", data["amount"], data["category"], message.text)
    await state.clear()
    from handlers.start import main_menu
    await message.answer(
        f"✅ Расход записан!\n\n"
        f"💸 Сумма: {data['amount']:,.0f} сум\n"
        f"📂 Категория: {data['category']}\n"
        f"📝 Описание: {message.text}",
        reply_markup=main_menu()
    )