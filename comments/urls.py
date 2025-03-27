from django.urls import path
from .views import CommentDelete, CommentEdit
from . import views

app_name = 'comments'

urlpatterns = [
    # Chemin pour supprimer un commentaire
    path('delete/<int:pk>/', CommentDelete.as_view(), name='delete'),
    path('edit/<int:pk>/', CommentEdit.as_view(), name='edit'),
    path('post/<int:pk>/', views.post_a_comment, name='post-comment')
]
