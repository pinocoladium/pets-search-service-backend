from collections.abc import Mapping


PET_SPECIES_MAP: Mapping[str, str] = {
    'DOG': '🐶 Собака',
    'CAT': '🐱 Кошка',
    'BIRD': '🐦 Птица',
    'OTHER': '🐾 Другое',
}

PET_SEX_MAP: Mapping[str, str] = {
    'MALE': '♂ Самец',
    'FEMALE': '♀ Самка',
    'UNKNOWN': '❓ Неизвестно',
}
