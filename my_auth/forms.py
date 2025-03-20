from django import forms
from django.forms import ModelForm
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

# je créé le formulaire pour les nouveaux users:
class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username','email', 'password1', 'password2')

    def clean_email(self) -> str:
        email: str = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Email already Used !')
        return email
    
# je créé le formulaire de connexion personnalisé :
class LoginForm(forms.Form):
    your_username = forms.CharField(max_length=200)
    your_password = forms.CharField(widget=forms.PasswordInput)