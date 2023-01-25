from loguru import logger
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.core.exceptions import ValidationError
from .serializers import GosNumberSerializer
from .models import GosNumber
from .numbers_gen import generate_gos_numbers


class GosNumberViewSet(ModelViewSet):
    queryset = GosNumber.objects.all()
    serializer_class = GosNumberSerializer
    permission_classes = [AllowAny]

    @action(methods=['get'], detail=False)
    def generate(self, request):
        # Метод для генерации указанного количества номеров
        amount = request.GET.get('amount')
        if not amount:
            number = generate_gos_numbers()
            logger.debug(f"Не передан amount, вывод одного номера: {number}")
            GosNumber.objects.create(number=number)
            last_gosnumber = GosNumber.objects.all().last()
            serializer = GosNumberSerializer(last_gosnumber)
            return Response(serializer.data, status=status.HTTP_200_OK)
        i = 0
        amount = int(amount)
        while i < amount:
            number = generate_gos_numbers()
            logger.debug(f"Gos Number: {number}")
            GosNumber.objects.create(number=number)
            i += 1
        gosnumbers = GosNumber.objects.all().order_by('-pk')[:amount]
        serializer = GosNumberSerializer(gosnumbers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def get(self, request):
        # Метод для вывода одной записи по uuid
        uuid = request.GET.get('id')
        if not uuid:
            return Response({'detail': 'Не передан uuid'})
        try:
            gosnumber_detail = GosNumber.objects.get(uuid=uuid)
            serializer = GosNumberSerializer(gosnumber_detail)
        except ValidationError:
            return Response({'detail': 'Неверный uuid'})
        return Response(serializer.data, status=status.HTTP_200_OK)
