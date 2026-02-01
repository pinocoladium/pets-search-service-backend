from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram.bot.contents import callbacks


def get_main_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text='Посмотреть список потерянных питомцев',
            callback_data=callbacks.PET_MISSING_NOTICES,
        )
    )
    builder.add(
        InlineKeyboardButton(
            text='Посмотреть список найденных питомцев',
            callback_data=callbacks.PET_FOUND_NOTICES,
        )
    )
    builder.add(
        InlineKeyboardButton(
            text='Посмотреть список ищущих дом питомцев',
            callback_data=callbacks.PET_ADOPTION_NOTICES,
        )
    )
    builder.add(
        InlineKeyboardButton(
            text='Посмотреть все объявления вокруг меня',
            callback_data=callbacks.ALL_NEAREST_NOTICES,
        )
    )
    builder.adjust(1)
    return builder.as_markup()


def get_more_details_keyboard(callback_data: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text='Подробнее',
            callback_data=callback_data,
        )
    )
    return builder.as_markup()


def get_back_keyboard(back_callback_data: str = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if back_callback_data:
        builder.add(
            InlineKeyboardButton(
                text='Обратно',
                callback_data=back_callback_data,
            )
        )
    builder.add(
        InlineKeyboardButton(
            text='В меню',
            callback_data=callbacks.MAIN_KEYBOARD,
        )
    )
    return builder.as_markup()


def get_add_anonymous_found_notice_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text='Оставить сообщение',
            callback_data=callbacks.ADD_ANONYMOUS_FOUND_NOTICE,
        )
    )
    return builder.as_markup()


def get_pet_species_keyboard() -> ReplyKeyboardMarkup:
    keys = [
        [
            KeyboardButton(text='Собака'),
            KeyboardButton(text='Кошка'),
            KeyboardButton(text='Птица'),
            KeyboardButton(text='Другое'),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=keys, resize_keyboard=True, input_field_placeholder='Выберите вид животного')


def get_pet_sex_keyboard() -> ReplyKeyboardMarkup:
    keys = [
        [
            KeyboardButton(text='Мальчик'),
            KeyboardButton(text='Девочка'),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=keys, resize_keyboard=True, input_field_placeholder='Выберите вид животного')


def get_location_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='📍 Отправить мою локацию', request_location=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
