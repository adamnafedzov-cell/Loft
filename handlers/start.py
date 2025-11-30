from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboards.main_menu import get_categories_kb
from utils.storage import user_state

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    table_id = "unknown"

    # Извлекаем стол из параметра start
    if "start=" in message.text:
        table_id = message.text.split("start=")[-1]

    # Сохраняем временное состояние
    user_state[message.from_user.id] = {
        "table": table_id
    }

    await message.answer(
        f"Здравствуйте! 👋\n"
        f"Спасибо, что решили оставить отзыв.\n\n"
        f"Стол: *{table_id}*\n"
        f"Выберите категорию:",
        reply_markup=get_categories_kb(),
        parse_mode="Markdown"
    )
