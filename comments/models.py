from django.db import models
from my_auth.models import CustomUser
from articles.models import Article
# Create your models here.

class Comment(models.Model):
    user: CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    article: Article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text: str = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'comment from {self.user} to {self.article}'