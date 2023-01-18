from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from loguru import logger
from .serializers import GosNumberSerializer
from .models import GosNumber
from .numbers_gen import gos_numbers_gen


class GosNumberViewSet(ModelViewSet):
    queryset = GosNumber.objects.all()
    serializer_class = GosNumberSerializer

    @action(methods=['get'], detail=False)
    def generate(self, request):
        amount = request.GET.get('amount')
        if not amount:
            number = gos_numbers_gen()
            logger.debug(f"Не передан amount, вывод одного номера: {number}")
            GosNumber.objects.create(number=number)
            gosnumber = GosNumber.objects.all().last()
            serializer = GosNumberSerializer(gosnumber)
            return Response(serializer.data)
        i = 0
        amount = int(amount)
        while i < amount:
            number = gos_numbers_gen()
            logger.debug(f"Gos Number: {number}")
            GosNumber.objects.create(number=number)
            i += 1
        gosnumbers = GosNumber.objects.all().order_by('-pk')[:amount]
        serializer = GosNumberSerializer(gosnumbers, many=True)
        return Response(serializer.data)
