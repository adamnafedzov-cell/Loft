from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboards.main_menu import get_categories_kb
from utils.storage import user_state
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(CommandStart())
async def start(message: Message):
    table_id = "unknown"
    # получаем аргументы после /start
    args = message.text.split(maxsplit=1)
    if len(args) > 1:
        payload = args[1]
        # допустим форматы: table_5 или start=table_5
        if "table_" in payload:
            table_id = payload.split("table_")[-1]
        else:
            table_id = payload.replace("start=", "")

    user_state[message.from_user.id] = {"table": table_id}
    await message.answer(
        f"Здравствуйте! 👋\nСпасибо, что решили оставить отзыв.\n\n📍 *Стол:* {table_id}\n\nВыберите категорию:",
        reply_markup=get_categories_kb(),
        parse_mode="Markdown"
    )
    logger.info("User started review flow for table %s", table_id)
