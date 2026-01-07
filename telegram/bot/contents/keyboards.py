from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
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
            text='Личный кабинет',
            callback_data=callbacks.PERSONAL_ACCOUNT,
        )
    )
    builder.adjust(1)
    return builder.as_markup()
