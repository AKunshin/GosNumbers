from rest_framework.viewsets import ModelViewSet
from .serializers import GosNumberSerializer
from .models import GosNumber
from .numbers_gen import gos_numbers_gen


class GosNumberViewSet(ModelViewSet):
    queryset = GosNumber.objects.all()
    serializer_class = GosNumberSerializer

class GenerateGosNumberViewSet(ModelViewSet):
    number = gos_numbers_gen()
    print(f"Gos Number {number}")
    GosNumber.objects.create(number=number)
    queryset = GosNumber.objects.all()
    serializer_class = GosNumberSerializer


# @api_view(['GET'])
# def generate(self, request):
#     number = gos_numbers_gen()
#     print(f"Gos Number {number}")
#     GosNumber.objects.create(number=number)
#     gosnumbers = GosNumber.objects.all()
#     serializer = GosNumberSerializer(gosnumbers, many=True)
#     return Response(serializer.data)
        

