from aiogram import Router, F
from aiogram.types import CallbackQuery
from utils.storage import user_state
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.callback_query(F.data.startswith("cat_"))
async def choose_category(callback: CallbackQuery):
    data = callback.data  # cat_food, cat_custom, cat_cancel
    user_id = callback.from_user.id

    if user_id not in user_state:
        user_state[user_id] = {}

    if data == "cat_cancel":
        user_state.pop(user_id, None)
        await callback.message.edit_text("Отмена. Если захотите оставить отзыв — снова отсканируйте QR-код. Спасибо!")
        await callback.answer()
        logger.info("User %s cancelled review flow", user_id)
        return

    category = data.replace("cat_", "")
    user_state[user_id]["category"] = category

    await callback.message.answer("Пожалуйста, напишите ваш отзыв ниже 👇")
    await callback.answer()
    logger.info("User %s chose category %s", user_id, category)
