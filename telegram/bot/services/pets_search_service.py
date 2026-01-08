from collections.abc import Iterable
from typing import Final

from telegram.bot.services.client import HttpClient
from telegram.bot.services.mappers import PET_SEX_MAP, PET_SPECIES_MAP


class PetsSearchService:
    PET_MISSING_NOTICES_API_URL: Final[str] = 'pet-missing-notices/'
    PET_FOUND_NOTICES_API_URL: Final[str] = 'pet-found-notices/'
    PET_ADOPTION_NOTICES_API_URL: Final[str] = 'pet-adoption-notices/'

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    async def get_active_pet_missing_notices(self) -> Iterable[str]:
        pet_missing_notices = await self._client.get(f'{self.PET_MISSING_NOTICES_API_URL}active/')
        return self._parse_pet_missing_notices(pet_missing_notices)

    async def get_active_pet_found_notices(self) -> Iterable[str]:
        pet_found_notices = await self._client.get(f'{self.PET_FOUND_NOTICES_API_URL}active/')
        return self._parse_pet_found_notices(pet_found_notices)

    async def get_active_pet_adoption_notices(self) -> Iterable[str]:
        pet_adoption_notices = await self._client.get(f'{self.PET_ADOPTION_NOTICES_API_URL}active/')
        return self._parse_pet_adoption_notices(pet_adoption_notices)

    def _parse_pet_missing_notices(self, pet_missing_notices: Iterable[dict]) -> Iterable[str]:
        result = []

        for pet_missing_notice in pet_missing_notices:
            text = self._format_common_fields(pet_missing_notice)
            text += f"<b>Время пропажи:</b> {pet_missing_notice['lost_datetime']}"
            result.append(text)

        return result

    def _parse_pet_found_notices(self, pet_found_notices: Iterable[dict]) -> Iterable[str]:
        result = []

        for pet_found_notice in pet_found_notices:
            text = self._format_common_fields(pet_found_notice)
            text += f"<b>Время обнаружения:</b> {pet_found_notice['found_datetime']}"
            result.append(text)

        return result

    def _parse_pet_adoption_notices(self, pet_adoption_notices: Iterable[dict]) -> Iterable[str]:
        return [self._format_common_fields(pet_adoption_notice) for pet_adoption_notice in pet_adoption_notices]

    @staticmethod
    def _format_common_fields(notice: dict) -> str:
        text = (
            f"🐾 <b>{notice['title']}</b>\n\n"
            f"<b>Кличка:</b> {notice['pet_name']}\n"
            f"<b>Вид:</b> {PET_SPECIES_MAP.get(notice['pet_species'], '—')}\n"
            f"<b>Пол:</b> {PET_SEX_MAP.get(notice['pet_sex'], '—')}\n"
            f"<b>Возраст:</b> {notice.get('pet_age') or 'не указан'}\n"
            f"<b>Порода:</b> {notice.get('pet_breed') or 'не указана'}\n"
            f"<b>Окрас:</b> {notice['pet_color']}\n"
        )

        if pet_special_marks := notice.get('pet_special_marks'):
            text += f"<b>Особые приметы:</b> {pet_special_marks}\n"

        text += f"\n<b>Описание:</b>\n{notice['description']}\n\n"

        return text
