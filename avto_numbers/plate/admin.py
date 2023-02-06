from django.contrib import admin
from .models import GosNumber

@admin.register(GosNumber)
class GosNumberAdmin(admin.ModelAdmin):
    list_display = ["id", "uuid", "number"]