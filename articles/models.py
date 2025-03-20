from django.db import models
from my_auth.models import CustomUser
# Create your models here.

class Article(models.Model):
    user: CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title: str = models.CharField(max_length=200)
    image = models.ImageField(upload_to='photo_articles/', blank=True, null=True)
    text: str = models.CharField(max_length=2000, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def like_count(self) -> int:
        # donne le nombre total de like de l'article:
        return LikeArticle.objects.filter(article=self, liked=True).count()
    
    def user_like(self, user: CustomUser) -> bool:
        # donne la value du like pour un user donné:
        # first() donne la premiere value sinon None : si le like n'existe pas envoie none:
        like_instance = LikeArticle.objects.filter(article=self, user=user).first()
        return like_instance.liked if like_instance else False


    def __str__(self) -> str:
        return self.title
    

class LikeArticle(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)

    # je créé une class pour que un user ne puisse faire l'action que une fois par article:
    class Meta:
        unique_together = ('user', 'article')

    def __str__(self) -> str:
        return f'Like for {self.article} from {self.user}'

    