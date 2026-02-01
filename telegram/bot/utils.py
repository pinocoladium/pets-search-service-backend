from datetime import date, datetime, timedelta

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from httpx import AsyncClient


async def clear_bot_messages(chat_id: int, state: FSMContext, bot) -> None:
    data = await state.get_data()
    message_ids = data.get('bot_messages', [])

    for message_id in reversed(message_ids):
        try:
            await bot.delete_message(chat_id, message_id)
        except TelegramBadRequest:
            pass

    await state.update_data(bot_messages=[])


async def save_bot_message(state: FSMContext, message) -> None:
    data = await state.get_data()
    messages = data.get('bot_messages', [])
    messages.append(message.message_id)
    await state.update_data(bot_messages=messages)


def parse_datetime(text: str) -> datetime | None:
    text = text.strip().lower()

    base_date = date.today()

    if text.startswith('сегодня'):
        text = text.replace('сегодня', '').strip()
    elif text.startswith('вчера'):
        base_date -= timedelta(days=1)
        text = text.replace('вчера', '').strip()

    try:
        found_time = datetime.strptime(text, '%H:%M').time()
        return datetime.combine(base_date, found_time)
    except ValueError:
        pass

    formats = [
        '%d.%m.%Y %H:%M',
        '%d/%m/%Y %H:%M',
        '%d-%m-%Y %H:%M',
        '%d.%m %H:%M',
        '%d/%m %H:%M',
        '%d-%m %H:%M',
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(text, fmt)
            if '%Y' not in fmt:
                dt = dt.replace(year=base_date.year)
            return dt
        except ValueError:
            continue

    return None


async def download_image(url: str) -> BufferedInputFile:
    async with AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()

        filename = url.split('/')[-1]

        return BufferedInputFile(
            response.content,
            filename=filename,
        )
