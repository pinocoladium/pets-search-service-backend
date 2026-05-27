from rest_framework import serializers


class OllamaGenerateResponseSerializer(serializers.Serializer):
    question = serializers.CharField(
        label='Вопрос',
        max_length=150,
    )


class OllamaImageDescriptionSerializer(serializers.Serializer):
    image = serializers.ImageField(
        label='Фотография',
    )
