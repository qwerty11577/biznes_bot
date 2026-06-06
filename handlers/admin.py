from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
import database as db

router = Router()

ADMIN_ID = 8257248746

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ У вас нет доступа!")
        return
    
    users = await db.get_all_users()
    text = "👑 Панель администратора\n"
    text += "━━━━━━━━━━━━━━━\n"
    text += f"👥 Всего пользователей: {len(users)} чел.\n\n"
    for user in users:
        user_id, username, full_name, joined, last_seen = user
        uname = f"@{username}" if username else "нет username"
        text += f"▪️ {full_name} ({uname})\n"
        text += f"   Зашёл: {last_seen[:10]}\n\n"
    
    await message.answer(text)

@router.message(Command("stats"))
async def admin_stats(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    
    users = await db.get_all_users()
    text = "📊 Статистика\n"
    text += "━━━━━━━━━━━━━━━\n"
    text += f"👥 Всего пользователей: {len(users)} чел.\n"
    
    await message.answer(text)