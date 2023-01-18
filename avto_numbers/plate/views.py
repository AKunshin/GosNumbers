from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import GosNumberSerializer
from .models import GosNumber
from .numbers_gen import gos_numbers_gen


class GosNumberViewSet(ModelViewSet):
    queryset = GosNumber.objects.all()
    serializer_class = GosNumberSerializer

    @action(methods=['get'], detail=False)
    def generate(self, request):
        number = gos_numbers_gen(2)
        print(f"Gos Number {number}")
        GosNumber.objects.create(number=number)
        gosnumbers = GosNumber.objects.all()
        serializer = GosNumberSerializer(gosnumbers, many=True)
        return Response(serializer.data)




        

