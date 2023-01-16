from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import GosNumberSerializer
from .models import GosNumber


class GosNumberViewSet(ModelViewSet):
    queryset = GosNumber.objects.all()
    serializer_class = GosNumberSerializer