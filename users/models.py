from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class user(AbstractUser):
    type = models.CharField(max_length=30)
    age = models.IntegerField(null=True)
    phone = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.name + ' '+self.type