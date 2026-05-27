from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.ai.serializers import (
    OllamaAnnouncementSerializer,
    OllamaGenerateResponseSerializer,
    OllamaPetDescriptionSerializer,
)
from apps.ai.services import OllamaService
from apps.ai.utils import check_announcement, generate_announcement_title, improve_announcement


class OllamaGenerateResponseAPIView(APIView):
    def post(self, request: Request) -> Response:
        serializer = OllamaGenerateResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = OllamaService().generate_response(serializer.validated_data['question'])

        return Response({'result': result})


class OllamaPetDescriptionAPIView(APIView):
    def post(self, request: Request) -> Response:
        serializer = OllamaPetDescriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        description = OllamaService().describe_image(
            serializer.validated_data['image'],
        )

        return Response({'description': description})


class OllamaImproveAnnouncementAPIView(APIView):
    def post(self, request: Request) -> Response:
        serializer = OllamaAnnouncementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        announcement = improve_announcement(
            serializer.validated_data['text'],
        )

        return Response({'announcement': announcement})


class OllamaGenerateAnnouncementTitleAPIView(APIView):
    def post(self, request: Request) -> Response:
        serializer = OllamaAnnouncementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        announcement_title = generate_announcement_title(
            serializer.validated_data['text'],
        )

        return Response({'announcement_title': announcement_title})


class OllamaCheckAnnouncementAPIView(APIView):
    def post(self, request: Request) -> Response:
        serializer = OllamaAnnouncementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        check_response = check_announcement(
            serializer.validated_data['text'],
        )

        return Response({'check_response': check_response})
