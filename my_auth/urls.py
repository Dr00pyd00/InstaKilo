from django.urls import path, include
from . import views

app_name = 'my_auth'

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login')
]