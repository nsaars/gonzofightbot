import random
import re
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from ..misc.states import FormStates
from tgbot.keyboards.reply import start, share_contact, step_back, submit
from aiogram.types import ReplyKeyboardRemove

questions = [
    "Напишите свое полное имя",
    "Дата рождения (11.11.1111)",
    "Какой у вас вес (в кг)?",
    "Какой у вас рост (в см)?",
    "В каком городе вы сейчас живете?",
    "Кто вы по национальности?",
    "Подробно опишите свои спортивные регалии",
    "Чем вы увлечены в жизни?",
    "Напишите, кем вы работаете или на кого учитесь",
    "Укажите свой логин в Instagram",
    "Напишите свой номер телефона (+998991234567)",
    "Когда был последний бой?",
    "Отправьте свое фото",
    "Отправьте видео 'Бой с тенью'",
    "Пришлите свой видеоклип, в котором вы рассказываете забавную историю, которая произошла с вами"
]

date_regex = re.compile(
    r"(\b(0?[1-9]|[12]\d|30|31)[^\w\d\r\n:](0?[1-9]|1[0-2])[^\w\d\r\n:](\d{4}|\d{2})\b)|(\b(0?[1-9]|1[0-2])[^\w\d\r\n:](0?[1-9]|[12]\d|30|31)[^\w\d\r\n:](\d{4}|\d{2})\b)")

phone_number_regex = re.compile(r"^(\+?\d{1,3}-?)?\d{2,3}-?\d{3}-?\d{2}-?\d{2}$")


async def start_handler(message: types.Message):
    if int(message.chat.id) < 0:
        await message.answer("Эту команду нельзя использовать в групповом чате.")
    await FormStates.START_SURVEY.set()
    await message.answer("""Вас приветствует официальный телеграмм бот GonzoFight 🫡

Чтобы попасть на 6 и 7 карды, вам нужно будет заполнить анкету

Каждый пункт анкеты важен. Подойдите к заполнению анкеты максимально серьезно, от этого будет зависеть выступаете вы у нас или нет 

Вы не сможете попасть к нам через знакомых, заплатив кому-то, придя к нам в офис или исполнив что-то еще. Участие в 
GonzoFight полностью бесплатное и происходит только на конкурентной основе. Все зависит только от вашей харизмы. 
Покажите ее в анкете и скорее всего вы будете выступать на GonzoFight""", reply_markup=start)


async def start_survey(message: types.Message):
    response = random.choice(["Если готов, напиши 'Поехали' !", "Напиши 'Поехали'", "Нажми на 'Поехали'."])
    if message.text == "Поехали":
        await FormStates.FULL_NAME.set()
        await message.answer(questions[0], reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(response)


async def full_name_handler(message: types.Message, state: FSMContext):
    answer = message.text.strip()
    await state.update_data(full_name=answer)
    await FormStates.DATE_OF_BIRTH.set()
    await message.answer(questions[1], reply_markup=step_back)


async def date_of_birth_handler(message: types.Message, state: FSMContext, order=2):
    if message.text == "Назад":
        await FormStates.FULL_NAME.set()
        await message.answer(questions[0], reply_markup=ReplyKeyboardRemove())
        return
    answer = message.text.strip()
    if not re.match(date_regex, answer):
        await message.reply("Недопустимый формат даты. Отправьте в формате 11.11.1111")
        return
    await state.update_data(date_of_birth=answer)
    await FormStates.WEIGHT.set()
    await message.answer(questions[2])


async def weight_handler(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FormStates.DATE_OF_BIRTH.set()
        await message.answer(questions[1], reply_markup=step_back)
        return
    answer = message.text.strip()
    await state.update_data(weight=answer)
    await FormStates.HEIGHT.set()
    await message.answer(questions[3])


async def height_handler(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FormStates.WEIGHT.set()
        await message.answer(questions[2])

        return
    answer = message.text.strip()
    await state.update_data(height=answer)
    await FormStates.CITY.set()
    await message.answer(questions[4])


async def city_handler(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FormStates.HEIGHT.set()
        await message.answer(questions[3])
        return
    answer = message.text.strip()
    await state.update_data(city=answer)
    await FormStates.NATIONALITY.set()
    await message.answer(questions[5])


async def nationality_handler(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FormStates.CITY.set()
        await message.answer(questions[4])
        return
    answer = message.text.strip()
    await state.update_data(nationality=answer)
    await FormStates.REGALIA.set()
    await message.answer(questions[6])


async def regalia_handler(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FormStates.NATIONALITY.set()
        await message.answer(questions[5])
        return
    answer = message.text.strip()
    await state.update_data(regalia=answer)
    await FormStates.PASSION.set()
    await message.answer(questions[7])


async def passion_handler(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FormStates.REGALIA.set()
        await message.answer(questions[6])
        return
    answer = message.text.strip()
    await state.update_data(passion=answer)
    await FormStates.WORK_OR_STUDY.set()
    await message.answer(questions[8])


async def work_or_study_handler(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FormStates.PASSION.set()
        await message.answer(questions[7])
        return
    answer = message.text.strip()
    await state.update_data(work_or_study=answer)
    await FormStates.INSTAGRAM.set()
    await message.answer(questions[9])


async def instagram_handler(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FormStates.WORK_OR_STUDY.set()
        await message.answer(questions[8])
        return
    answer = message.text.strip()
    await state.update_data(instagram=answer)
    await FormStates.PHONE_NUMBER.set()
    await message.answer(questions[10], reply_markup=share_contact)


async def phone_number_handler(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FormStates.INSTAGRAM.set()
        await message.answer(questions[9], reply_markup=step_back)
        return
    answer = ''
    if message.content_type == "text":
        answer = message.text.strip()
        if not re.match(phone_number_regex, answer):
            await message.reply("Неверный формат телефонного номера. Отправьте в формате +998901234567")
            return
    elif message.content_type == "contact":
        answer = message.contact.phone_number

    await state.update_data(phone_number=answer)
    await FormStates.LAST_FIGHT_DATE.set()
    await message.answer(questions[11], reply_markup=step_back)


async def last_fight_date_handler(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FormStates.PHONE_NUMBER.set()
        await message.answer(questions[10], reply_markup=share_contact)
        return
    answer = message.text.strip()
    await state.update_data(last_fight_date=answer)
    await FormStates.PHOTO.set()
    await message.answer(questions[12])


async def photo_handler(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FormStates.LAST_FIGHT_DATE.set()
        await message.answer(questions[11])
        return
    response = random.choice(["Очень интересно, но я фото просил.", "Suratingizni yuboring, birodar.", "Это не фото."])
    if message.content_type == "document":
        await message.reply(f"Формат файла не подходит.")
        return
    elif message.content_type != "photo":
        await message.reply(response)
        return

    answer = f"Photo: {message.photo[-1].file_id}"
    await state.update_data(photo=answer)
    await FormStates.SHADOW_FIGHT_VIDEO.set()
    await message.answer(questions[13])


async def wrong_video_format(message: types.Message, response: str):
    if message.text == "Назад":
        await FormStates.FULL_NAME.set()
        await message.answer(questions[0])
        return
    if message.content_type == "document":
        await message.reply(f"Формат файла не подходит.")
        return True
    elif message.content_type == "video_note":
        await message.reply("Дружище, видеокружок не подходит, у нас серьёзная организация.")
        return True
    elif message.content_type != "video":
        await message.reply(response)
        return True
    return False


async def shadow_fight_video_handler(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FormStates.PHOTO.set()
        await message.answer(questions[12])
        return
    response = random.choice(
        ["Видео это когда картинки двигаются.", "Videoni yuboring 'Soya bilan jang'", "Это не видео."])
    if await wrong_video_format(message, response):
        return
    answer = f"Video: {message.video.file_id}"
    await state.update_data(shadow_fight_video=answer)
    await FormStates.FUNNY_STORY_VIDEO.set()
    await message.answer(questions[14])


async def funny_story_video_handler(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await FormStates.SHADOW_FIGHT_VIDEO.set()
        await message.answer(questions[13])
        return
    response = random.choice(
        ["Во первых, это не видео, а во вторых, это несмешно.",
         "Siz bilan sodir bo'lgan kulgili voqeani aytib beradigan videoklipingizni yuboring", "Это не видео."])
    if await wrong_video_format(message, response):
        return
    answer = f"Video: {message.video.file_id}"
    await state.update_data(funny_story_video=answer)
    await FormStates.SUBMIT_FORM.set()
    await submit_form(message, state)


async def submit_form(message, state):
    data = await state.get_data()
    message_text = f"username: {message.from_user.username}\n"
    media_group = []
    regex = r"^(Photo|Video):(.+)$"

    for i, d in enumerate(data, 1):
        if d != 'media_group':
            d_ = re.sub(r"\s", "", data[d])
            match = re.match(regex, d_)
            if match:
                type_, id_ = match.groups()[0], match.groups()[1]
                args = (id_, message_text) if len(media_group) == 0 else (id_,)
                if type_ == "Photo":
                    media_group.append(types.InputMediaPhoto(*args))
                elif type_ == "Video":
                    media_group.append(types.InputMediaVideo(*args))
            else:
                message_text += f"{i}. {data[d]}\n"
    await state.update_data(media_group=media_group)
    await message.bot.send_media_group(chat_id=message.from_user.id, media=media_group)
    await message.answer("Проверьте вашу форму и нажмите \"Отправить\".", reply_markup=submit)


async def send_form(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == "Отправить":
        await message.answer(f"{message.from_user.full_name}, вы закончили регистрацию. Ожидайте, с вами свяжутся.",
                             reply_markup=ReplyKeyboardRemove())

        for admin in message.bot['config'].tg_bot.admin_ids:
            await message.bot.send_media_group(chat_id=admin, media=data["media_group"])
        await state.reset_state(with_data=True)
    elif message.text == "Заполнить заново":
        await FormStates.FULL_NAME.set()
        await message.answer(questions[0], reply_markup=ReplyKeyboardRemove())
    elif message.text == "Назад":
        await FormStates.FUNNY_STORY_VIDEO.set()
        await message.answer(questions[14], reply_markup=step_back)


def register_survey(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'], state="*")
    dp.register_message_handler(start_survey, state=FormStates.START_SURVEY)
    dp.register_message_handler(full_name_handler, state=FormStates.FULL_NAME)
    dp.register_message_handler(date_of_birth_handler, state=FormStates.DATE_OF_BIRTH)
    dp.register_message_handler(weight_handler, state=FormStates.WEIGHT)
    dp.register_message_handler(height_handler, state=FormStates.HEIGHT)
    dp.register_message_handler(city_handler, state=FormStates.CITY)
    dp.register_message_handler(nationality_handler, state=FormStates.NATIONALITY)
    dp.register_message_handler(regalia_handler, state=FormStates.REGALIA)
    dp.register_message_handler(passion_handler, state=FormStates.PASSION)
    dp.register_message_handler(work_or_study_handler, state=FormStates.WORK_OR_STUDY)
    dp.register_message_handler(instagram_handler, state=FormStates.INSTAGRAM)
    dp.register_message_handler(phone_number_handler, state=FormStates.PHONE_NUMBER, content_types=["text", "contact"])
    dp.register_message_handler(last_fight_date_handler, state=FormStates.LAST_FIGHT_DATE)
    dp.register_message_handler(photo_handler, state=FormStates.PHOTO, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(shadow_fight_video_handler, state=FormStates.SHADOW_FIGHT_VIDEO,
                                content_types=types.ContentTypes.ANY)
    dp.register_message_handler(funny_story_video_handler, state=FormStates.FUNNY_STORY_VIDEO,
                                content_types=types.ContentTypes.ANY)
    dp.register_message_handler(send_form, state=FormStates.SUBMIT_FORM,
                                content_types=types.ContentTypes.ANY)
