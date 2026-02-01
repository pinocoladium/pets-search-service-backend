import os

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from telegram.bot.contents import callbacks, keyboards, messages
from telegram.bot.utils import clear_bot_messages, download_image, save_bot_message


class NearestNoticesFSM(StatesGroup):
    waiting_location = State()


router = Router()


def get_pets_search_service():
    from telegram.bot.services.client import DjangoHttpClient
    from telegram.bot.services.pets_search_service import PetsSearchService

    http_client = DjangoHttpClient(os.getenv('DJANGO_BASE_API_URL'))
    return PetsSearchService(http_client)


@router.callback_query(F.data == callbacks.ALL_NEAREST_NOTICES)
async def handle_ready_waiting_location(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer(messages.CALLBACK_ANSWER_MESSAGE)
    await clear_bot_messages(chat_id=callback.message.chat.id, state=state, bot=callback.bot)
    await state.clear()

    await state.set_state(NearestNoticesFSM.waiting_location)

    bot_message = await callback.message.answer(
        '📍 Отправь свою локацию, и я покажу ближайшие объявления', reply_markup=keyboards.get_location_keyboard()
    )
    await save_bot_message(state, bot_message)


@router.message(NearestNoticesFSM.waiting_location)
async def handle_get_all_nearest_notices(message: Message, state: FSMContext) -> None:
    await clear_bot_messages(chat_id=message.chat.id, state=state, bot=message.bot)
    await state.clear()

    location = message.location

    bot_message = await message.answer('🔍 Ищу все объявления рядом с тобой...', reply_markup=None)
    await save_bot_message(state, bot_message)

    point = f'SRID=4326;POINT ({location.longitude} {location.latitude})'

    pet_missing_notices = await get_pets_search_service().get_active_pet_missing_notices(point=point)
    pet_found_notices = await get_pets_search_service().get_active_pet_found_notices(point=point)

    if not pet_missing_notices and not pet_found_notices:
        bot_message = await message.answer(
            '😔 Поблизости ничего не найдено', reply_markup=keyboards.get_back_keyboard()
        )
        await save_bot_message(state, bot_message)
        return

    if pet_missing_notices:
        bot_message = await message.answer('Следующие питомцы были потеряны возле Вас 👇')
        await save_bot_message(state, bot_message)
        for pet_missing_notice in pet_missing_notices:
            bot_message = await message.answer(
                pet_missing_notice['short_text'],
                parse_mode='HTML',
                reply_markup=keyboards.get_more_details_keyboard(
                    f'nearest_{callbacks.PET_MISSING_NOTICES_DETAILS}:{pet_missing_notice['id']}'
                ),
            )
            await save_bot_message(state, bot_message)

    if pet_found_notices:
        bot_message = await message.answer('Следующие животные найдены возле Вас 👇')
        await save_bot_message(state, bot_message)
        for pet_found_notice in pet_found_notices:
            bot_message = await message.answer(
                pet_found_notice['short_text'],
                parse_mode='HTML',
                reply_markup=keyboards.get_more_details_keyboard(
                    f'nearest_{callbacks.PET_FOUND_NOTICES_DETAILS}:{pet_found_notice['id']}'
                ),
            )
            await save_bot_message(state, bot_message)

    bot_message = await message.answer(messages.BACK_TO_MAIN_MESSAGE, reply_markup=keyboards.get_back_keyboard())
    await save_bot_message(state, bot_message)


@router.callback_query(F.data.startswith(f'nearest_{callbacks.PET_MISSING_NOTICES_DETAILS}'))
async def handle_get_nearest_pet_missing_notices_details(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer(messages.CALLBACK_ANSWER_MESSAGE)
    await clear_bot_messages(chat_id=callback.message.chat.id, state=state, bot=callback.bot)

    _, object_id = callback.data.split(':')
    pet_missing_notices = await get_pets_search_service().get_active_pet_missing_notices(int(object_id))

    for pet_missing_notice in pet_missing_notices:
        bot_message = await callback.message.answer_photo(
            photo=await download_image(pet_missing_notice['image_url']),
            caption=pet_missing_notice['full_text'],
            parse_mode='HTML',
            reply_markup=keyboards.get_back_keyboard(),
        )
        await save_bot_message(state, bot_message)


@router.callback_query(F.data.startswith(f'nearest_{callbacks.PET_FOUND_NOTICES_DETAILS}'))
async def handle_get_nearest_pet_found_notices_details(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer(messages.CALLBACK_ANSWER_MESSAGE)
    await clear_bot_messages(chat_id=callback.message.chat.id, state=state, bot=callback.bot)

    _, object_id = callback.data.split(':')
    pet_found_notices = await get_pets_search_service().get_active_pet_found_notices(int(object_id))

    for pet_found_notice in pet_found_notices:
        bot_message = await callback.message.answer_photo(
            photo=await download_image(pet_found_notice['image_url']),
            caption=pet_found_notice['full_text'],
            parse_mode='HTML',
            reply_markup=keyboards.get_back_keyboard(),
        )
        await save_bot_message(state, bot_message)
