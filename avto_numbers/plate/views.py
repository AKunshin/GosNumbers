from loguru import logger
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .serializers import GosNumberSerializer
from .models import GosNumber
from .service import generate_gos_numbers, validate_number


class GosNumberViewSet(ModelViewSet):
    queryset = GosNumber.objects.all()
    serializer_class = GosNumberSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["get"], detail=False)
    def generate(self, request):
        """ Метод для генерации указанного количества номеров """
        amount = request.GET.get("amount")
        if amount:
            amount = int(amount)
        else:
            amount = 1
        new_numbers = generate_gos_numbers(amount)
        for new_number in new_numbers:
            # Проверка на наличие сгенерированных номеров в БД
            while GosNumber.objects.filter(number=new_number).exists():
                new_number = generate_gos_numbers(1)
            GosNumber.objects.create(number=new_number)
        gosnumbers = GosNumber.objects.all().order_by("-pk")[:amount]
        serializer = GosNumberSerializer(gosnumbers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def get(self, request):
        """ Метод для вывода одной записи по uuid """
        uuid = request.GET.get("id")
        # Из GET-запроса получаем значение id
        if not uuid:
            return Response(
                {"detail": "Не передан uuid"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            gosnumber_detail = get_object_or_404(GosNumber, uuid=uuid)
            serializer = GosNumberSerializer(gosnumber_detail)
        except ValidationError:
            return Response(
                {"detail": "Неверный uuid"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=False)
    def add(self, request):
        # Метод для добавления переданного клиентом гос.номера в БД
        plate = request.data.get("plate")
        # Из POST-запроса получаем значение plate
        logger.debug(f"Полученный номер: {plate}")
        if not plate:
            return Response(
                {"detail": "Не передан гос. номер"},
                status=status.HTTP_400_BAD_REQUEST
            )
        plate = plate.upper()
        if not validate_number(plate):
            return Response(
                {"detail": "Ошибка в гос. номере"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if GosNumber.objects.filter(number=plate).exists():
            return Response(
                {"detail": "Данный гос. номер уже содержится в БД"},
                status=status.HTTP_400_BAD_REQUEST)
        new_number = GosNumber.objects.create(number=plate)
        serializer = GosNumberSerializer(new_number)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
