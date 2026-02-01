import os

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from telegram.bot.contents import callbacks, keyboards, messages
from telegram.bot.handlers.mappers import PET_SEX_MAP, PET_SPECIES_MAP
from telegram.bot.services.client import DjangoHttpClient
from telegram.bot.services.pets_search_service import PetsSearchService
from telegram.bot.utils import clear_bot_messages, parse_datetime, save_bot_message


class AnonymousFoundPetFSM(StatesGroup):
    title = State()
    description = State()
    pet_name = State()
    pet_species = State()
    pet_breed = State()
    pet_color = State()
    pet_special_marks = State()
    pet_sex = State()
    found_datetime = State()
    found_location = State()
    image = State()


router = Router()


@router.callback_query(F.data == callbacks.ADD_ANONYMOUS_FOUND_NOTICE)
async def handle_add_anonymous_found_notice(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer(messages.CALLBACK_ANSWER_MESSAGE)
    await clear_bot_messages(chat_id=callback.message.chat.id, state=state, bot=callback.bot)
    await state.clear()
    await state.set_state(AnonymousFoundPetFSM.title)

    bot_message = await callback.message.answer('🐾 Введите заголовок для объявления (например: «Найден рыжий кот»)')
    await save_bot_message(state, bot_message)


@router.message(AnonymousFoundPetFSM.title)
async def handle_set_title_anonymous_found_notice(message: Message, state: FSMContext) -> None:
    await clear_bot_messages(chat_id=message.chat.id, state=state, bot=message.bot)
    await state.update_data(title=message.text)

    await state.set_state(AnonymousFoundPetFSM.description)
    bot_message = await message.answer('✏️ Опишите по возможности самого питомца и обстоятельства находки')
    await save_bot_message(state, bot_message)


@router.message(AnonymousFoundPetFSM.description)
async def handle_set_description_anonymous_found_notice(message: Message, state: FSMContext) -> None:
    await clear_bot_messages(chat_id=message.chat.id, state=state, bot=message.bot)
    await state.update_data(description=message.text)

    await state.set_state(AnonymousFoundPetFSM.pet_name)
    bot_message = await message.answer('🐕 Кличка, на которую откликается животное, если неизвестно, напишите "-"')
    await save_bot_message(state, bot_message)


@router.message(AnonymousFoundPetFSM.pet_name)
async def handle_set_pet_name_anonymous_found_notice(message: Message, state: FSMContext) -> None:
    await clear_bot_messages(chat_id=message.chat.id, state=state, bot=message.bot)
    await state.update_data(pet_name=message.text)

    await state.set_state(AnonymousFoundPetFSM.pet_species)
    bot_message = await message.answer(
        '🐾 Выберите на клавиатуре вид животного',
        reply_markup=keyboards.get_pet_species_keyboard(),
    )
    await save_bot_message(state, bot_message)


@router.message(AnonymousFoundPetFSM.pet_species, F.text)
async def handle_set_pet_species_anonymous_found_notice(message: Message, state: FSMContext) -> None:
    await clear_bot_messages(chat_id=message.chat.id, state=state, bot=message.bot)
    text = message.text.strip()

    if text not in {'Собака', 'Кошка', 'Птица', 'Другое'}:
        bot_message = await message.answer(
            'Выберите вариант с кнопки 👇', reply_markup=keyboards.get_pet_species_keyboard()
        )
        await save_bot_message(state, bot_message)
        return

    await state.update_data(pet_species=text)
    await state.set_state(AnonymousFoundPetFSM.pet_breed)
    bot_message = await message.answer('📌 Порода (если неизвестна — напишите «-»)', reply_markup=None)
    await save_bot_message(state, bot_message)


@router.message(AnonymousFoundPetFSM.pet_breed)
async def handle_set_pet_breed_anonymous_found_notice(message: Message, state: FSMContext) -> None:
    await clear_bot_messages(chat_id=message.chat.id, state=state, bot=message.bot)
    await state.update_data(pet_breed=message.text)

    await state.set_state(AnonymousFoundPetFSM.pet_color)
    bot_message = await message.answer(
        '🐾 Напиши приблизительный окрас питомца - цвет и узор покрова (шерсти, кожи, перьев)'
    )
    await save_bot_message(state, bot_message)


@router.message(AnonymousFoundPetFSM.pet_color)
async def handle_set_pet_color_anonymous_found_notice(message: Message, state: FSMContext) -> None:
    await clear_bot_messages(chat_id=message.chat.id, state=state, bot=message.bot)
    await state.update_data(pet_color=message.text)

    await state.set_state(AnonymousFoundPetFSM.pet_special_marks)
    bot_message = await message.answer(
        '🐾 Может есть какие-нибудь особые приметы питомца? Если есть, опиши их, пожалуйста'
    )
    await save_bot_message(state, bot_message)


@router.message(AnonymousFoundPetFSM.pet_special_marks)
async def handle_set_pet_special_marks_anonymous_found_notice(message: Message, state: FSMContext) -> None:
    await clear_bot_messages(chat_id=message.chat.id, state=state, bot=message.bot)
    await state.update_data(pet_special_marks=message.text)

    await state.set_state(AnonymousFoundPetFSM.pet_sex)
    bot_message = await message.answer(
        '🐾 Укажи на клавиатуре пол животного',
        reply_markup=keyboards.get_pet_sex_keyboard(),
    )
    await save_bot_message(state, bot_message)


@router.message(AnonymousFoundPetFSM.pet_sex, F.text)
async def handle_set_pet_sex_anonymous_found_notice(message: Message, state: FSMContext) -> None:
    await clear_bot_messages(chat_id=message.chat.id, state=state, bot=message.bot)
    text = message.text.strip()

    if text not in {'Мальчик', 'Девочка'}:
        bot_message = await message.answer(
            'Выберите вариант с кнопки 👇', reply_markup=keyboards.get_pet_sex_keyboard()
        )
        await save_bot_message(state, bot_message)
        return

    await state.update_data(pet_sex=text)
    await state.set_state(AnonymousFoundPetFSM.found_datetime)
    bot_message = await message.answer(
        '🐾 В какое время было найдено животное? '
        'Напиши дату и время в формате ДД.ММ.ГГГГ ЧЧ:ММ, либо - "сегодня 14:30" или "вчера 21:15"',
        reply_markup=None,
    )
    await save_bot_message(state, bot_message)


@router.message(AnonymousFoundPetFSM.found_datetime, F.text)
async def handle_set_found_datetime_anonymous_found_notice(message: Message, state: FSMContext) -> None:
    await clear_bot_messages(chat_id=message.chat.id, state=state, bot=message.bot)
    found_datetime = parse_datetime(message.text)

    if not found_datetime:
        bot_message = await message.answer(
            '❌ Не смог распознать дату и время.\n\n'
            'Примеры:\n'
            '• 12.01.2025 14:30\n'
            '• сегодня 14:30\n'
            '• вчера 21:15'
        )
        await save_bot_message(state, bot_message)
        return

    await state.update_data(found_datetime=found_datetime)
    await state.set_state(AnonymousFoundPetFSM.found_location)
    bot_message = await message.answer('📍 Где было найдено животное? Отправь, пожалуйста, геопозицию')
    await save_bot_message(state, bot_message)


@router.message(AnonymousFoundPetFSM.found_location, F.location)
async def handle_set_found_location_anonymous_found_notice(message: Message, state: FSMContext) -> None:
    await clear_bot_messages(chat_id=message.chat.id, state=state, bot=message.bot)
    location = message.location

    await state.update_data(found_location=f'SRID=4326;POINT ({location.longitude} {location.latitude})')

    await state.set_state(AnonymousFoundPetFSM.image)
    bot_message = await message.answer('📸 Пришли фото питомца', reply_markup=None)
    await save_bot_message(state, bot_message)


@router.message(AnonymousFoundPetFSM.image, F.photo)
async def handle_set_image_anonymous_found_notice(message: Message, state: FSMContext) -> None:
    await clear_bot_messages(chat_id=message.chat.id, state=state, bot=message.bot)
    try:
        photo = message.photo[-1]

        file_info = await message.bot.get_file(photo.file_id)
        image_stream = await message.bot.download_file(file_info.file_path)
        await state.update_data(image_bytes=image_stream.getvalue())

        await finish_and_send_to_api(message, state)

    except Exception:
        bot_message = await message.answer('⚠️ Не удалось обработать фото. Попробуйте ещё раз.')
        await save_bot_message(state, bot_message)


async def finish_and_send_to_api(message: Message, state: FSMContext) -> None:
    await clear_bot_messages(chat_id=message.chat.id, state=state, bot=message.bot)
    try:
        data = await state.get_data()
        image_bytes = data.get('image_bytes')

        if not image_bytes:
            bot_message = await message.answer('⚠️ Фото не найдено. Попробуйте отправить снова.')
            await save_bot_message(state, bot_message)
            return

        request_data = {
            'title': data['title'],
            'description': data['description'],
            'pet_name': data['pet_name'],
            'pet_species': PET_SPECIES_MAP[data['pet_species']],
            'pet_breed': data['pet_breed'],
            'pet_color': data['pet_color'],
            'pet_special_marks': data['pet_special_marks'],
            'pet_sex': PET_SEX_MAP[data['pet_sex']],
            'found_datetime': data['found_datetime'].isoformat(),
            'found_location': data['found_location'],
        }

        http_client = DjangoHttpClient(os.getenv('DJANGO_BASE_API_URL'))
        pets_search_service = PetsSearchService(http_client)

        try:
            await pets_search_service.create_anonymous_found_notice(request_data=request_data, image_bytes=image_bytes)
        except Exception:
            bot_message = await message.answer(
                '⚠️ Произошла ошибка при создании объявления. Попробуйте позже.',
                reply_markup=keyboards.get_back_keyboard(),
            )
            await save_bot_message(state, bot_message)
            await state.clear()
            return

        await state.clear()
        bot_message = await message.answer(
            '✅ Объявление успешно создано! '
            'После прохождения модерации Ваше объявление появится в списке активных\nБольшое спасибо ❤️',
            reply_markup=keyboards.get_back_keyboard(),
        )
        await save_bot_message(state, bot_message)

    except Exception:
        bot_message = await message.answer(
            '⚠️ Произошла внутренняя ошибка. Попробуйте снова.',
            reply_markup=keyboards.get_back_keyboard(),
        )
        await save_bot_message(state, bot_message)
        await state.clear()
