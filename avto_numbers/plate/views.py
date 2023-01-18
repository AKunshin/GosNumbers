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
        logger.debug(request)
        gen_number = gos_numbers_gen(3)
        i = 0
        while i < 3:
            number = gen_number[i]
            logger.debug(f"Gos Number {number}")
            GosNumber.objects.create(number=number)
            i += 1
        gosnumbers = GosNumber.objects.all().order_by('-pk')[:3]
        serializer = GosNumberSerializer(gosnumbers, many=True)
        return Response(serializer.data)




        

