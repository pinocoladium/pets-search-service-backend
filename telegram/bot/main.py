import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from telegram.bot.contents import callbacks, keyboards, messages, stickers
from telegram.bot.services.client import HttpClient
from telegram.bot.services.pets_search_service import PetsSearchService


logging.basicConfig(level=logging.INFO)

telegram_bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))

dispatcher = Dispatcher()

http_client = HttpClient(os.getenv('DJANGO_BASE_API_URL'))
pets_search_service = PetsSearchService(http_client)


@dispatcher.message(CommandStart())
async def handle_start_command(message: Message) -> None:
    await telegram_bot.send_sticker(chat_id=message.chat.id, sticker=stickers.GREETING_STICKER)
    await message.answer(messages.GREETING_MESSAGE)
    await message.answer(messages.MAIN_KEYBOARD_MESSAGE, reply_markup=keyboards.get_main_keyboard())


@dispatcher.callback_query(F.data == callbacks.PET_MISSING_NOTICES)
async def handle_get_pet_missing_notices(callback: CallbackQuery) -> None:
    await callback.answer(messages.CALLBACK_ANSWER_MESSAGE)
    await callback.message.answer(messages.PET_MISSING_NOTICES_MESSAGE)

    pet_missing_notices = await pets_search_service.get_active_pet_missing_notices()

    if not pet_missing_notices:
        await callback.message.answer(messages.NO_NOTICES_MESSAGE)
        return

    for pet_missing_notice in pet_missing_notices:
        await callback.message.answer(pet_missing_notice, parse_mode='HTML')


@dispatcher.callback_query(F.data == callbacks.PET_FOUND_NOTICES)
async def handle_get_pet_found_notices(callback: CallbackQuery) -> None:
    await callback.answer(messages.CALLBACK_ANSWER_MESSAGE)
    await callback.message.answer(messages.PET_FOUND_NOTICES_MESSAGE)

    pet_found_notices = await pets_search_service.get_active_pet_found_notices()

    if not pet_found_notices:
        await callback.message.answer(messages.NO_NOTICES_MESSAGE)
        return

    for pet_found_notice in pet_found_notices:
        await callback.message.answer(pet_found_notice, parse_mode='HTML')


@dispatcher.callback_query(F.data == callbacks.PET_ADOPTION_NOTICES)
async def handle_get_pet_adoption_notices(callback: CallbackQuery) -> None:
    await callback.answer(messages.CALLBACK_ANSWER_MESSAGE)
    await callback.message.answer(messages.PET_ADOPTION_NOTICES_MESSAGE)

    pet_adoption_notices = await pets_search_service.get_active_pet_adoption_notices()

    if not pet_adoption_notices:
        await callback.message.answer(messages.NO_NOTICES_MESSAGE)
        return

    for pet_adoption_notice in pet_adoption_notices:
        await callback.message.answer(pet_adoption_notice, parse_mode='HTML')


@dispatcher.callback_query(F.data == callbacks.PERSONAL_ACCOUNT)
async def handle_get_personal_account(callback: CallbackQuery) -> None:
    await callback.answer(messages.CALLBACK_ANSWER_MESSAGE)
    await callback.message.answer(messages.PERSONAL_ACCOUNT_MESSAGE)


async def on_shutdown() -> None:
    await http_client.close()


async def main() -> None:
    dispatcher.shutdown.register(on_shutdown)
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dispatcher.start_polling(telegram_bot)


if __name__ == '__main__':
    asyncio.run(main())
