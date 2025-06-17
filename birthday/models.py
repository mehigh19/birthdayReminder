from django.db import models

class birthDay(models.Model):
    name = models.CharField(max_length=50)
    bDayDate = models.DateField()