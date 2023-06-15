import re
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

questions = [
    "Напишите свое полное имя:",
    "Дата рождения (11.11.1111):",
    "Какой у вас вес (в кг)?:",
    "Какой у вас рост (в см)?:",
    "В каком городе вы сейчас живете?:",
    "Кто вы по национальности?:",
    "Подробно опишите свои спортивные регалии:",
    "Чем вы увлечены в жизни?:",
    "Напишите, кем вы работаете или на кого учитесь:",
    "Укажите свой логин в Instagram:",
    "Напишите свой номер телефона (+998991234567):",
    "Когда был последний бой (11.11.1111)?:",
    "Отправьте свое фото:",
    "Отправьте видео 'Бой с тенью':",
    "Пришлите свой видеоклип, в котором вы рассказываете забавную историю, которая произошла с вами:"
]

date_regex = re.compile(
    r"(\b(0?[1-9]|[12]\d|30|31)[^\w\d\r\n:](0?[1-9]|1[0-2])[^\w\d\r\n:](\d{4}|\d{2})\b)|(\b(0?[1-9]|1[0-2])[^\w\d\r\n:](0?[1-9]|[12]\d|30|31)[^\w\d\r\n:](\d{4}|\d{2})\b)")

phone_number_regex = re.compile(r"^(\+?998-?)?\d{2}-?\d{3}-?\d{2}-?\d{2}$")


class FormStates(StatesGroup):
    FULL_NAME = State()
    DATE_OF_BIRTH = State()
    WEIGHT = State()
    HEIGHT = State()
    CITY = State()
    NATIONALITY = State()
    REGALIA = State()
    PASSION = State()
    WORK_OR_STUDY = State()
    INSTAGRAM = State()
    PHONE_NUMBER = State()
    LAST_FIGHT_DATE = State()
    PHOTO = State()
    SHADOW_FIGHT_VIDEO = State()
    FUNNY_STORY_VIDEO = State()


async def start_handler(message: types.Message, state: FSMContext):
    await FormStates.FULL_NAME.set()
    await message.answer(questions[0])


async def full_name_handler(message: types.Message, state: FSMContext):
    answer = message.text.strip()
    await state.update_data(full_name=answer)
    await FormStates.DATE_OF_BIRTH.set()
    await message.answer(questions[1])


async def date_of_birth_handler(message: types.Message, state: FSMContext):
    answer = message.text.strip()
    if not re.match(date_regex, answer):
        await message.reply("Invalid date format.")
        return
    await state.update_data(date_of_birth=answer)
    await FormStates.WEIGHT.set()
    await message.answer(questions[2])


async def weight_handler(message: types.Message, state: FSMContext):
    answer = message.text.strip()
    await state.update_data(weight=answer)
    await FormStates.HEIGHT.set()
    await message.answer(questions[3])


async def height_handler(message: types.Message, state: FSMContext):
    answer = message.text.strip()
    await state.update_data(height=answer)
    await FormStates.CITY.set()
    await message.answer(questions[4])


async def city_handler(message: types.Message, state: FSMContext):
    answer = message.text.strip()
    await state.update_data(city=answer)
    await FormStates.NATIONALITY.set()
    await message.answer(questions[5])


async def nationality_handler(message: types.Message, state: FSMContext):
    answer = message.text.strip()
    await state.update_data(nationality=answer)
    await FormStates.REGALIA.set()
    await message.answer(questions[6])


async def regalia_handler(message: types.Message, state: FSMContext):
    answer = message.text.strip()
    await state.update_data(regalia=answer)
    await FormStates.PASSION.set()
    await message.answer(questions[7])


async def passion_handler(message: types.Message, state: FSMContext):
    answer = message.text.strip()
    await state.update_data(passion=answer)
    await FormStates.WORK_OR_STUDY.set()
    await message.answer(questions[8])


async def work_or_study_handler(message: types.Message, state: FSMContext):
    answer = message.text.strip()
    await state.update_data(work_or_study=answer)
    await FormStates.INSTAGRAM.set()
    await message.answer(questions[9])


async def instagram_handler(message: types.Message, state: FSMContext):
    answer = message.text.strip()
    await state.update_data(instagram=answer)
    await FormStates.PHONE_NUMBER.set()
    await message.answer(questions[10])


async def phone_number_handler(message: types.Message, state: FSMContext):
    answer = message.text.strip()
    if not re.match(phone_number_regex, answer):
        await message.reply("Invalid phone number format.")
        return
    await state.update_data(phone_number=answer)
    await FormStates.LAST_FIGHT_DATE.set()
    await message.answer(questions[11])


async def last_fight_date_handler(message: types.Message, state: FSMContext):
    answer = message.text.strip()
    if not re.match(date_regex, answer):
        await message.reply("Invalid date format.")
        return
    await state.update_data(last_fight_date=answer)
    await FormStates.PHOTO.set()
    await message.answer(questions[12])


async def photo_handler(message: types.Message, state: FSMContext):
    answer = f"Photo: {message.photo[-1].file_id}"
    await state.update_data(photo=answer)
    await FormStates.SHADOW_FIGHT_VIDEO.set()
    await message.answer(questions[13])


async def shadow_fight_video_handler(message: types.Message, state: FSMContext):
    answer = f"Video: {message.video.file_id}"
    await state.update_data(shadow_fight_video=answer)
    await FormStates.FUNNY_STORY_VIDEO.set()
    await message.answer(questions[14])


async def funny_story_video_handler(message: types.Message, state: FSMContext):
    answer = f"Video: {message.video.file_id}"
    await state.update_data(funny_story_video=answer)
    await message.answer(f"{message.from_user.full_name}, вы закончили регистрацию. Ожидайте, с вами свяжутся.")
    await submit_form(message, state)


async def submit_form(message, state):
    data = await state.get_data()
    bot = message.bot
    message_text = f"username: {message.from_user.username}\n"
    media_group = []
    regex = r"^(Photo|Video):(.+)$"

    for i, d in enumerate(data, 1):
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
    await bot.send_media_group(chat_id=bot['config'].tg_bot.admin_ids[0], media=media_group)
    await state.finish()


def register_survey(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'], state="*")
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
    dp.register_message_handler(phone_number_handler, state=FormStates.PHONE_NUMBER)
    dp.register_message_handler(last_fight_date_handler, state=FormStates.LAST_FIGHT_DATE)
    dp.register_message_handler(photo_handler, state=FormStates.PHOTO, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(shadow_fight_video_handler, state=FormStates.SHADOW_FIGHT_VIDEO,
                                content_types=types.ContentTypes.VIDEO)
    dp.register_message_handler(funny_story_video_handler, state=FormStates.FUNNY_STORY_VIDEO,
                                content_types=types.ContentTypes.VIDEO)
