from aiogram import Router
from aiogram.types import Message
from utils.storage import user_state
from config import ADMIN_GROUP_ID
import db
import logging
from datetime import datetime
import html

logger = logging.getLogger(__name__)
router = Router()

@router.message()
async def get_review(message: Message):
    user_id = message.from_user.id

    if user_id not in user_state:
        return

    data = user_state[user_id]
    table = data.get("table", "unknown")
    category = data.get("category", "unknown")
    review_text = message.text.strip()
    if not review_text:
        await message.answer("Пожалуйста, напишите непустой отзыв.")
        return

    # Сохраняем в базу
    created_at = datetime.utcnow().isoformat()
    try:
        await db.insert_review(table, category, review_text, created_at)
    except Exception as e:
        logger.exception("DB insert error: %s", e)

    # Отправляем в админ-группу (экранить HTML-символы)
    safe_text = html.escape(review_text)
    admin_message = (
        f"📍 *Стол:* {table}\n"
        f"📂 *Категория:* {category}\n"
        f"🕒 *Время:* {created_at} UTC\n\n"
        f"📝 *Отзыв:*\n{safe_text}"
    )

    try:
        await message.bot.send_message(ADMIN_GROUP_ID, admin_message, parse_mode="Markdown")
    except Exception:
        # если Markdown ломается, шлём просто текст
        await message.bot.send_message(ADMIN_GROUP_ID, f"Стол: {table}\nКатегория: {category}\n\n{review_text}")

    logger.info("New review saved: table=%s category=%s", table, category)

    await message.answer("Спасибо за ваш отзыв! ❤️")
    user_state.pop(user_id, None)

