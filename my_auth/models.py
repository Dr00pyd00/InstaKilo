from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


# je créé mon model User personnalisable:
class CustomUser(AbstractUser):
    pass