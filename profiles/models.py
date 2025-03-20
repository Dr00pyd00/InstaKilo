from django.db import models
from datetime import date
from my_auth.models import CustomUser

# Create your models here.

class ProfileModel(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    birth_day = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=300)
    profile_photo = models.ImageField(upload_to='photos_profiles/', null=True, blank=True )
    presentation = models.CharField(max_length=1000, null=True, blank=True)

    def age(self) -> int:
        if self.birth_day:
            today = date.today()
            return today.year - self.birth_day.year - ((today.month, today.day) < (self.birth_day.month, self.birth_day.day))
        return None
    
    def __str__(self) -> str:
        return self.user.username
        