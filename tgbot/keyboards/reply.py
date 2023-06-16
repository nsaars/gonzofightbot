from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start = ReplyKeyboardMarkup([[KeyboardButton("Поехали")]], resize_keyboard=True)

share_contact = ReplyKeyboardMarkup([[KeyboardButton("Поделиться номером", request_contact=True)]], resize_keyboard=True)