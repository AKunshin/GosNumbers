import uuid
from django.db import models


class GosNumber(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True,
                          default=uuid.uuid4, unique=True,
                          editable=False, verbose_name="Id")
    number = models.CharField(max_length=6, verbose_name="Гос. номер авто")

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = "Гос. номер"
        verbose_name_plural = "Гос. номера"
