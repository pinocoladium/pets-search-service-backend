from aiogram.fsm.context import FSMContext


async def clear_bot_messages(chat_id: int, state: FSMContext, bot) -> None:
    data = await state.get_data()
    message_ids = data.get('bot_messages', [])

    for message_id in message_ids:
        await bot.delete_message(chat_id, message_id)

    await state.update_data(bot_messages=[])


async def save_bot_message(state: FSMContext, message) -> None:
    data = await state.get_data()
    messages = data.get('bot_messages', [])
    messages.append(message.message_id)
    await state.update_data(bot_messages=messages)
