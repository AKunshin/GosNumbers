import re
from loguru import logger
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.exceptions import ValidationError
from .serializers import GosNumberSerializer
from .models import GosNumber
from .numbers_gen import generate_gos_numbers


class GosNumberViewSet(ModelViewSet):
    queryset = GosNumber.objects.all()
    serializer_class = GosNumberSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=False)
    def generate(self, request):
        # Метод для генерации указанного количества номеров
        amount = request.GET.get('amount')
        if not amount:
            number = generate_gos_numbers()
            logger.debug(f"Не передан amount, вывод одного номера: {number}")
            last_gosnumber = GosNumber.objects.create(number=number)
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
            return Response({'detail': 'Не передан uuid'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            gosnumber_detail = GosNumber.objects.get(uuid=uuid)
            serializer = GosNumberSerializer(gosnumber_detail)
        except ValidationError:
            return Response({'detail': 'Неверный uuid'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['post'], detail=False)
    def add(self, request):
        # Метод для добавления переданного клиентом гос.номера в БД
        plate = request.GET.get('plate').upper()
        logger.debug(f"Полученный номер: {plate}")
        if not plate:
            return Response({'detail':'Не передан гос. номер'}, status=status.HTTP_400_BAD_REQUEST)
        tpl = r'[АВЕКМНОРСТУХ]{1}\d{3}[АВЕКМНОРСТУХ]{2}$'
        if not re.match(tpl, plate):
            return Response({'detail': 'Ошибка в гос. номере'}, status=status.HTTP_400_BAD_REQUEST)
        new_number = GosNumber.objects.create(number=plate)
        serializer = GosNumberSerializer(new_number)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

