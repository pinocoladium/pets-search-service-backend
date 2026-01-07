import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from telegram.bot.contents import callbacks, keyboards, messages, stickers


logging.basicConfig(level=logging.INFO)

telegram_bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))

dispatcher = Dispatcher()


@dispatcher.message(CommandStart())
async def handle_start_command(message: Message) -> None:
    await telegram_bot.send_sticker(chat_id=message.chat.id, sticker=stickers.GREETING_STICKER)
    await message.answer(messages.GREETING_MESSAGE)
    await message.answer(messages.MAIN_KEYBOARD_MESSAGE, reply_markup=keyboards.get_main_keyboard())


@dispatcher.callback_query(F.data == callbacks.PET_MISSING_NOTICES)
async def handle_get_pet_missing_notices(callback: CallbackQuery):
    await callback.message.answer(messages.PET_MISSING_NOTICES_MESSAGE)


@dispatcher.callback_query(F.data == callbacks.PET_FOUND_NOTICES)
async def handle_get_pet_found_notices(callback: CallbackQuery):
    await callback.message.answer(messages.PET_FOUND_NOTICES_MESSAGE)


@dispatcher.callback_query(F.data == callbacks.PET_ADOPTION_NOTICES)
async def handle_get_pet_adoption_notices(callback: CallbackQuery):
    await callback.message.answer(messages.PET_ADOPTION_NOTICES_MESSAGE)


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dispatcher.start_polling(telegram_bot)


if __name__ == '__main__':
    asyncio.run(main())
