from django.urls import path, include
from . import views

app_name = 'profiles'

urlpatterns = [
        path('creation/', views.ProfileCreate, name='create-profile'),
        path('my_profile/', views.ProfileShow, name='my-profile'),
        path('edit/', views.ProfileEdit, name='edit-profil'),
        path('doublon/', views.ProfilDoublon, name='doublon'),
        path('delete/', views.ProfileDelete, name='delete-profile')
        
]