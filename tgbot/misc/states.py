from aiogram.dispatcher.filters.state import State, StatesGroup


class FormStates(StatesGroup):
    START_SURVEY = State()
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
    SUBMIT_FORM = State()

