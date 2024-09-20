from django.db import models
from datetime import timedelta


class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.CharField(max_length=10, null=True)
    durations = models.DurationField(null=False, default=timedelta(hours=1))

    def __str__(self):
        return self.name
    
class FreeDate(models.Model):
    date = models.CharField(max_length=10, unique=True) 
    free = models.BooleanField(default=True, null=False)

    def __str__(self):
        return self.date


class Notes(models.Model):
    name = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=15, null=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.CharField(null=False, blank=True)
    time = models.CharField(null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Errors(models.Model):
    name = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=15, null=False)
    description = models.TextField(null=False)
