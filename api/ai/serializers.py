from rest_framework import serializers


class OllamaGenerateResponseSerializer(serializers.Serializer):
    question = serializers.CharField(
        label='Вопрос',
        max_length=150,
    )


class OllamaPetDescriptionSerializer(serializers.Serializer):
    image = serializers.ImageField(
        label='Фотография',
    )


class OllamaAnnouncementSerializer(serializers.Serializer):
    text = serializers.CharField(
        label='Текст объявления',
        max_length=150,
    )
