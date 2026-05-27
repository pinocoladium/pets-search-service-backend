from apps.ai.services import OllamaService


def improve_announcement(text: str) -> str:
    prompt = (
        'Улучши текст объявления о животном. '
        'Пиши только на русском языке. '
        'Не добавляй факты, которых нет в тексте. '
        'Сделай текст понятным, спокойным и коротким.\n\n'
        f'Текст: {text}'
    )
    return OllamaService().generate_response(prompt)


def generate_announcement_title(text: str) -> str:
    prompt = (
        'Сгенерируй короткий заголовок для объявления о животном. '
        'Максимум 5 слов. '
        'Не выдумывай факты.\n\n'
        f'Текст объявления: {text}'
    )
    return OllamaService().generate_response(prompt)


def check_announcement(text: str) -> str:
    words_count = len(text.split())

    if words_count <= 20:
        return 'Не хватает подробностей: объявление должно быть больше ...'

    prompt = (
        'Ты проверяешь объявление о животном. '
        'Ответь только одним из двух форматов:\n'
        '1. "Объявление заполнено достаточно подробно"\n'
        '2. "Не хватает: ..."\n\n'
        'Проверь наличие: место, дата, цвет, особые приметы, контакты. '
        'Не оценивай стиль. Не выдумывай данные.\n\n'
        f'Объявление: {text}'
    )

    return OllamaService().generate_response(prompt)
