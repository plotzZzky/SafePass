from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    db = models.CharField(max_length=4096)
    db_pwd = models.CharField(max_length=255)
