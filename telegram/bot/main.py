import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from httpx import AsyncClient

from telegram.bot.contents import callbacks, keyboards, messages, stickers
from telegram.bot.services.client import DjangoHttpClient
from telegram.bot.services.pets_search_service import PetsSearchService
from telegram.bot.utils import clear_bot_messages, save_bot_message


logging.basicConfig(level=logging.INFO)

telegram_bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))

dispatcher = Dispatcher()

http_client = DjangoHttpClient(os.getenv('DJANGO_BASE_API_URL'))
pets_search_service = PetsSearchService(http_client)


@dispatcher.message(CommandStart())
async def handle_start_command(message: Message, state: FSMContext) -> None:
    sticker_message = await telegram_bot.send_sticker(chat_id=message.chat.id, sticker=stickers.GREETING_STICKER)
    await save_bot_message(state, sticker_message)
    bot_message = await message.answer(messages.GREETING_MESSAGE)
    await save_bot_message(state, bot_message)
    bot_message = await message.answer(messages.MAIN_KEYBOARD_MESSAGE, reply_markup=keyboards.get_main_keyboard())
    await save_bot_message(state, bot_message)


@dispatcher.callback_query(F.data == callbacks.MAIN_KEYBOARD)
async def handle_main_keyboard_command(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer(messages.CALLBACK_ANSWER_MESSAGE)
    await clear_bot_messages(
        chat_id=callback.message.chat.id,
        state=state,
        bot=callback.bot,
    )

    bot_message = await callback.message.answer(
        messages.MAIN_KEYBOARD_MESSAGE, reply_markup=keyboards.get_main_keyboard()
    )
    await save_bot_message(state, bot_message)


@dispatcher.callback_query(F.data == callbacks.PET_MISSING_NOTICES)
async def handle_get_pet_missing_notices(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer(messages.CALLBACK_ANSWER_MESSAGE)

    await clear_bot_messages(
        chat_id=callback.message.chat.id,
        state=state,
        bot=callback.bot,
    )

    pet_missing_notices = await pets_search_service.get_active_pet_missing_notices()

    if not pet_missing_notices:
        sticker_message = await telegram_bot.send_sticker(
            chat_id=callback.message.chat.id, sticker=stickers.NO_NOTICES_STICKER
        )
        await save_bot_message(state, sticker_message)
        bot_message = await callback.message.answer(
            messages.NO_NOTICES_MESSAGE, reply_markup=keyboards.get_back_keyboard()
        )
        await save_bot_message(state, bot_message)
        return

    bot_message = await callback.message.answer(messages.PET_MISSING_NOTICES_MESSAGE)
    await save_bot_message(state, bot_message)
    for pet_missing_notice in pet_missing_notices:
        bot_message = await callback.message.answer(
            pet_missing_notice['short_text'],
            parse_mode='HTML',
            reply_markup=keyboards.get_more_details_keyboard(
                f'{callbacks.PET_MISSING_NOTICES_DETAILS}:{pet_missing_notice['id']}'
            ),
        )
        await save_bot_message(state, bot_message)


@dispatcher.callback_query(F.data.startswith(callbacks.PET_MISSING_NOTICES_DETAILS))
async def handle_get_pet_missing_notices_details(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer(messages.CALLBACK_ANSWER_MESSAGE)
    await clear_bot_messages(
        chat_id=callback.message.chat.id,
        state=state,
        bot=callback.bot,
    )

    _, object_id = callback.data.split(':')
    pet_missing_notices = await pets_search_service.get_active_pet_missing_notices(int(object_id))

    for pet_missing_notice in pet_missing_notices:
        bot_message = await callback.message.answer_photo(
            photo=await download_image(pet_missing_notice['image_url']),
            caption=pet_missing_notice['full_text'],
            parse_mode='HTML',
            reply_markup=keyboards.get_back_keyboard(callbacks.PET_MISSING_NOTICES),
        )
        await save_bot_message(state, bot_message)


@dispatcher.callback_query(F.data == callbacks.PET_FOUND_NOTICES)
async def handle_get_pet_found_notices(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer(messages.CALLBACK_ANSWER_MESSAGE)
    await clear_bot_messages(
        chat_id=callback.message.chat.id,
        state=state,
        bot=callback.bot,
    )

    pet_found_notices = await pets_search_service.get_active_pet_found_notices()

    if not pet_found_notices:
        sticker_message = await telegram_bot.send_sticker(
            chat_id=callback.message.chat.id, sticker=stickers.NO_NOTICES_STICKER
        )
        await save_bot_message(state, sticker_message)
        bot_message = await callback.message.answer(
            messages.NO_NOTICES_MESSAGE, reply_markup=keyboards.get_back_keyboard()
        )
        await save_bot_message(state, bot_message)
        return

    bot_message = await callback.message.answer(messages.PET_FOUND_NOTICES_MESSAGE)
    await save_bot_message(state, bot_message)
    for pet_found_notice in pet_found_notices:
        bot_message = await callback.message.answer(
            pet_found_notice['short_text'],
            parse_mode='HTML',
            reply_markup=keyboards.get_more_details_keyboard(
                f'{callbacks.PET_FOUND_NOTICES_DETAILS}:{pet_found_notice['id']}'
            ),
        )
        await save_bot_message(state, bot_message)


@dispatcher.callback_query(F.data.startswith(callbacks.PET_FOUND_NOTICES_DETAILS))
async def handle_get_pet_found_notices_details(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer(messages.CALLBACK_ANSWER_MESSAGE)
    await clear_bot_messages(
        chat_id=callback.message.chat.id,
        state=state,
        bot=callback.bot,
    )

    _, object_id = callback.data.split(':')
    pet_found_notices = await pets_search_service.get_active_pet_found_notices(int(object_id))

    for pet_found_notice in pet_found_notices:
        bot_message = await callback.message.answer_photo(
            photo=await download_image(pet_found_notice['image_url']),
            caption=pet_found_notice['full_text'],
            parse_mode='HTML',
            reply_markup=keyboards.get_back_keyboard(callbacks.PET_FOUND_NOTICES),
        )
        await save_bot_message(state, bot_message)


@dispatcher.callback_query(F.data == callbacks.PET_ADOPTION_NOTICES)
async def handle_get_pet_adoption_notices(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer(messages.CALLBACK_ANSWER_MESSAGE)
    await clear_bot_messages(
        chat_id=callback.message.chat.id,
        state=state,
        bot=callback.bot,
    )

    pet_adoption_notices = await pets_search_service.get_active_pet_adoption_notices()

    if not pet_adoption_notices:
        sticker_message = await telegram_bot.send_sticker(
            chat_id=callback.message.chat.id, sticker=stickers.NO_NOTICES_STICKER
        )
        await save_bot_message(state, sticker_message)
        bot_message = await callback.message.answer(
            messages.NO_NOTICES_MESSAGE, reply_markup=keyboards.get_back_keyboard()
        )
        await save_bot_message(state, bot_message)
        return

    bot_message = await callback.message.answer(messages.PET_ADOPTION_NOTICES_MESSAGE)
    await save_bot_message(state, bot_message)
    for pet_adoption_notice in pet_adoption_notices:
        bot_message = await callback.message.answer(
            pet_adoption_notice['short_text'],
            parse_mode='HTML',
            reply_markup=keyboards.get_more_details_keyboard(
                f'{callbacks.PET_ADOPTION_NOTICES_DETAILS}:{pet_adoption_notice['id']}'
            ),
        )
        await save_bot_message(state, bot_message)


@dispatcher.callback_query(F.data.startswith(callbacks.PET_ADOPTION_NOTICES_DETAILS))
async def handle_get_pet_adoption_notices_details(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer(messages.CALLBACK_ANSWER_MESSAGE)
    await clear_bot_messages(
        chat_id=callback.message.chat.id,
        state=state,
        bot=callback.bot,
    )

    _, object_id = callback.data.split(':')
    pet_adoption_notices = await pets_search_service.get_active_pet_adoption_notices(int(object_id))

    for pet_adoption_notice in pet_adoption_notices:
        bot_message = await callback.message.answer_photo(
            photo=await download_image(pet_adoption_notice['image_url']),
            caption=pet_adoption_notice['full_text'],
            parse_mode='HTML',
            reply_markup=keyboards.get_back_keyboard(callbacks.PET_ADOPTION_NOTICES),
        )
        await save_bot_message(state, bot_message)


@dispatcher.callback_query(F.data == callbacks.PERSONAL_ACCOUNT)
async def handle_get_personal_account(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer(messages.CALLBACK_ANSWER_MESSAGE)
    await clear_bot_messages(
        chat_id=callback.message.chat.id,
        state=state,
        bot=callback.bot,
    )

    sticker_message = await telegram_bot.send_sticker(chat_id=callback.message.chat.id, sticker=stickers.PLUG_STICKER)
    await save_bot_message(state, sticker_message)
    bot_message = await callback.message.answer(
        messages.PERSONAL_ACCOUNT_MESSAGE, reply_markup=keyboards.get_back_keyboard()
    )
    await save_bot_message(state, bot_message)


async def on_shutdown() -> None:
    await http_client.close()


async def download_image(url: str) -> BufferedInputFile:
    async with AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()

        filename = url.split('/')[-1]

        return BufferedInputFile(
            response.content,
            filename=filename,
        )


async def main() -> None:
    dispatcher.shutdown.register(on_shutdown)
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dispatcher.start_polling(telegram_bot)


if __name__ == '__main__':
    asyncio.run(main())
