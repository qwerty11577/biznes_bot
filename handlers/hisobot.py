from aiogram import Router, F
from aiogram.types import Message
import database as db

router = Router()

@router.message(F.text == "📊 Отчёт")
async def hisobot(message: Message):
    user_id = message.from_user.id
    daromad, xarajat = await db.get_summary(user_id)
    foyda = daromad - xarajat
    transactions = await db.get_transactions(user_id, limit=5)
    debts = await db.get_debts(user_id)
    products = await db.get_products(user_id)

    text = "📊 Отчёт\n"
    text += "━━━━━━━━━━━━━━━\n"
    text += f"💰 Доходы:  {daromad:,.0f} сум\n"
    text += f"💸 Расходы: {xarajat:,.0f} сум\n"
    text += f"📈 Прибыль: {foyda:,.0f} сум\n"
    text += "━━━━━━━━━━━━━━━\n\n"

    if transactions:
        text += "🕐 Последние операции:\n"
        for t in transactions:
            type_, amount, category, desc, date = t
            emoji = "💰" if type_ == "daromad" else "💸"
            text += f"{emoji} {category} — {amount:,.0f} сум\n"
        text += "\n"

    if debts:
        text += "👥 Активные долги:\n"
        menga = sum(d[2] for d in debts if d[3] == "menga")
        menda = sum(d[2] for d in debts if d[3] == "mendан")
        text += f"🔴 Мне должны: {menga:,.0f} сум\n"
        text += f"🟢 Я должен: {menda:,.0f} сум\n\n"

    if products:
        text += "📦 Товары на складе:\n"
        total = sum(p[2] * p[3] for p in products)
        text += f"▪️ Позиций: {len(products)} шт\n"
        text += f"💎 Общая стоимость: {total:,.0f} сум\n"

    from handlers.start import main_menu
    await message.answer(text, reply_markup=main_menu())