from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboards.main_menu import get_categories_kb
from utils.storage import user_state

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    table_id = "unknown"

    # Все способы получения параметра
    args = message.text.split(maxsplit=1)
    if len(args) > 1:
        table_id = args[1].replace("start=", "")

    user_state[message.from_user.id] = {"table": table_id}

    await message.answer(
        f"Здравствуйте! 👋\n"
        f"Спасибо, что решили оставить отзыв.\n\n"
        f"Стол: *{table_id}*\n"
        f"Выберите категорию:",
        reply_markup=get_categories_kb(),
        parse_mode="Markdown"
    )
