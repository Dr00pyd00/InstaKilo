from django import forms
from django.forms import ModelForm
from .models import ProfileModel


# je creer le formulaire a remplir pour le profile general :
class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        #fields = '__all__'
        exclude = ['user']