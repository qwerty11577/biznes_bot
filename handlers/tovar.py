from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import database as db

router = Router()

class TovarState(StatesGroup):
    name = State()
    quantity = State()
    price = State()
    unit = State()

def cancel_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Отмена")]],
        resize_keyboard=True
    )

@router.message(F.text == "📦 Товары")
async def tovar_start(message: Message, state: FSMContext):
    await state.set_state(TovarState.name)
    await message.answer("📦 Введите название товара:", reply_markup=cancel_keyboard())

@router.message(TovarState.name)
async def tovar_name(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        from handlers.start import main_menu
        await message.answer("Отменено.", reply_markup=main_menu())
        return
    await state.update_data(name=message.text)
    await state.set_state(TovarState.quantity)
    await message.answer("📊 Введите количество:")

@router.message(TovarState.quantity)
async def tovar_quantity(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        from handlers.start import main_menu
        await message.answer("Отменено.", reply_markup=main_menu())
        return
    try:
        quantity = float(message.text.replace(",", "."))
        await state.update_data(quantity=quantity)
        await state.set_state(TovarState.price)
        await message.answer("💰 Введите цену за единицу:")
    except ValueError:
        await message.answer("❗ Введите число. Например: 100")

@router.message(TovarState.price)
async def tovar_price(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        from handlers.start import main_menu
        await message.answer("Отменено.", reply_markup=main_menu())
        return
    try:
        price = float(message.text.replace(",", "."))
        await state.update_data(price=price)
        await state.set_state(TovarState.unit)
        await message.answer("📏 Введите единицу измерения (шт, кг, л, м):")
    except ValueError:
        await message.answer("❗ Введите число. Например: 15000")

@router.message(TovarState.unit)
async def tovar_unit(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        from handlers.start import main_menu
        await message.answer("Отменено.", reply_markup=main_menu())
        return
    data = await state.get_data()
    await db.add_product(message.from_user.id, data["name"], data["quantity"], data["price"], message.text)
    await state.clear()
    from handlers.start import main_menu
    await message.answer(
        f"✅ Товар добавлен!\n\n"
        f"📦 Название: {data['name']}\n"
        f"📊 Количество: {data['quantity']} {message.text}\n"
        f"💰 Цена: {data['price']:,.0f} сум",
        reply_markup=main_menu()
    )

@router.message(F.text == "📋 Список товаров")
async def tovar_list(message: Message):
    products = await db.get_products(message.from_user.id)
    if not products:
        from handlers.start import main_menu
        await message.answer("📭 Товаров нет!", reply_markup=main_menu())
        return
    text = "📦 Список товаров:\n\n"
    total = 0
    for product in products:
        id_, name, quantity, price, unit = product
        summa = quantity * price
        total += summa
        text += f"▪️ {name}\n   {quantity} {unit} × {price:,.0f} = {summa:,.0f} сум\n\n"
    text += f"💎 Общая стоимость: {total:,.0f} сум"
    from handlers.start import main_menu
    await message.answer(text, reply_markup=main_menu())