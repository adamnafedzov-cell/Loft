from aiogram import Router, F
from aiogram.types import CallbackQuery
from utils.storage import user_state

router = Router()

@router.callback_query(F.data.startswith("cat_"))
async def choose_category(callback: CallbackQuery):
    category = callback.data.replace("cat_", "")
    user_state[callback.from_user.id]["category"] = category

    await callback.message.answer(
        "Пожалуйста, напишите ваш отзыв 👇"
    )

    await callback.answer()
