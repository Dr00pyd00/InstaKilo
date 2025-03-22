from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('my_articles/', views.ArticlesList, name='my-articles'),
    path('detail/<int:pk>', views.ArticleDetail, name='detail'),
    path('create/', views.ArticleCreate, name='create-article'),
    path('update/<int:pk>/', views.ArticleUpdate,name='update'),
    path('delete/<int:pk>', views.ArticleDelete, name='delete'),

    path('like/<int:article_id>', views.LikeOfArticle, name='like-statut'),   # gestion du like/unlike

        
]