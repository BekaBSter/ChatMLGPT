from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Выбор нейросети"), KeyboardButton(text="Профиль"), KeyboardButton(text="Контакты")]
], resize_keyboard=True)

change_neuro = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="ChatGPT", callback_data="neuro_ChatGPT")],
    [InlineKeyboardButton(text="Gemini", callback_data="neuro_Gemini")],
    [InlineKeyboardButton(text="DALL-E", callback_data="neuro_DALL-E")]
])

reg_answer = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да", callback_data="reg_yes")],
    [InlineKeyboardButton(text="Нет", callback_data="reg_no")]
])
