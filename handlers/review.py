from aiogram import Router
from aiogram.types import Message
from utils.storage import user_state
from config import ADMIN_GROUP_ID

router = Router()

@router.message()
async def get_review(message: Message):

    user_id = message.from_user.id

    if user_id not in user_state:
        return

    data = user_state[user_id]
    table = data.get("table")
    category = data.get("category")
    review_text = message.text

    # Отправка в админ-группу
    await message.bot.send_message(
        ADMIN_GROUP_ID,
        f"📍 *Стол:* {table}\n"
        f"📂 *Категория:* {category}\n"
        f"📝 *Отзыв:*\n{review_text}",
        parse_mode="Markdown"
    )

    await message.answer("Спасибо за ваш отзыв! ❤️")

    # Удаляем состояние
    user_state.pop(user_id, None)
