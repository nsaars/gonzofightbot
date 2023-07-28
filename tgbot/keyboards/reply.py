from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start = ReplyKeyboardMarkup([[KeyboardButton("Поехали")]], resize_keyboard=True)

share_contact = ReplyKeyboardMarkup(
    [[KeyboardButton("Поделиться номером", request_contact=True)], [KeyboardButton("Назад")]], resize_keyboard=True)

step_back = ReplyKeyboardMarkup([[KeyboardButton("Назад")]], resize_keyboard=True)

submit = ReplyKeyboardMarkup(
    [[KeyboardButton("Отправить"), KeyboardButton("Заполнить заново")], [KeyboardButton("Назад")]],
    resize_keyboard=True)
