from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_categories_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🍽 Еда", callback_data="cat_food")],
        [InlineKeyboardButton(text="🥤 Напитки", callback_data="cat_drink")],
        [InlineKeyboardButton(text="😊 Обслуживание", callback_data="cat_service")],
        [InlineKeyboardButton(text="✨ Атмосфера", callback_data="cat_atmo")],
        [InlineKeyboardButton(text="🧼 Чистота", callback_data="cat_clean")],
        [InlineKeyboardButton(text="✏️ Свой вариант", callback_data="cat_custom")],
    ])
