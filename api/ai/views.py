from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.ai.serializers import OllamaGenerateResponseSerializer, OllamaImageDescriptionSerializer
from apps.ai.services import OllamaService


class OllamaGenerateResponseAPIView(APIView):
    def post(self, request: Request) -> Response:
        serializer = OllamaGenerateResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = OllamaService().generate_response(serializer.validated_data['question'])

        return Response({'result': result})


class OllamaImageDescriptionAPIView(APIView):
    def post(self, request: Request) -> Response:
        serializer = OllamaImageDescriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        description = OllamaService().describe_image(
            serializer.validated_data['image'],
        )

        return Response({'description': description})
