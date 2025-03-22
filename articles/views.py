from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from .models import Article, LikeArticle
from .forms import ArticleForm
from django.contrib import messages
from comments.forms import CommentForm
from comments.models import Comment
from my_auth.models import CustomUser
from typing import Dict, List

# Create your views here.


def ArticlesList(request: HttpRequest) -> HttpResponse:
    articles: Article = Article.objects.filter(user=request.user).order_by('-create_date')  # Trier par date descendante
    ctx: dict[str, Article] = {'articles':articles}
    return render(request, 'articles/articles_list.html', ctx)
    



def ArticleCreate(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            new_article = form.save(commit=False)
            new_article.user = request.user
            new_article.save()
            return redirect('articles:my-articles')
    else:
        form = ArticleForm()
    ctx: Dict[str, ArticleForm] ={'form':form}
    return render(request, 'articles/create_article.html', ctx)





def ArticleUpdate(request: HttpRequest,pk:int) -> HttpResponse:
    article: Article = get_object_or_404(Article,pk=pk )
    if request.user != article.user:
        return redirect('articles:my-articles')
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
             form.save()
             return redirect('articles:my-articles')

    else:
        form = ArticleForm(instance=article)
    ctx: Dict[str, ArticleForm] = {'form':form}
    return render(request, 'articles/update_article.html', ctx)






def ArticleDelete(request: HttpRequest, pk: int) -> HttpResponse:
    article: Article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        if request.POST.get('delete'):
            article.delete()
            messages.warning(request, f'You deleted the article : {article.title}.')
            return redirect('articles:my-articles')
        else:
            messages.info(request, 'You canceled the delete of your article !')
            return redirect('articles:my-articles')

    ctx: Dict[str, Article] = {'article':article}
    return render(request, 'articles/delete_article.html', ctx)



def ArticleDetail(request: HttpRequest, pk: int) -> HttpResponse:
    article: Article = get_object_or_404(Article, pk=pk)

    # je compte le nombre de likes total:
    like_count: int = article.like_count()
    
    # je check si un object like existe deja, sinon ca envoie None (.first()),
    # puis je vais chercher le statut du like si il existe:
    user_like_statut: LikeArticle = LikeArticle.objects.filter(user=request.user, article=article).first()

    if request.method == 'POST':

        # gestion des likes:
        if 'like' in request.POST:
            # si user a deja like on inverse le bool:
            if user_like_statut:
                user_like_statut.liked = not user_like_statut.liked 
                user_like_statut.save()
            else:
                LikeArticle.objects.create(user=request.user, article=article, liked=True)
            return redirect('articles:detail', pk=pk)
        
        # gestion des commentaires:
        form: CommentForm = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.article = article
            comment.save()
            return redirect('articles:detail', pk=pk)
        
        # get method:
    else:
        form: CommentForm = CommentForm()
    # recuperation des commentaires de l'article:
    comments: List[Comment] = article.comment_set.all()

    ctx: Dict[str, Article | List[Comment] | CommentForm | LikeArticle] = {
        'article':article,
        'comments':comments,
        'form':form,
        'user_like_statut':user_like_statut,
        'like_count':like_count
        }
    
    return render(request, 'articles/article_detail.html', ctx)


# vue pour mettre un like ou le passer en unlike en boucle:
def LikeOfArticle(request, article_id):

    if request.method == 'POST':
        # je chope l'article :
        article = get_object_or_404(Article, pk= article_id)

        # je check si request.user a deja like ou pas :
        user_like_statut = LikeArticle.objects.filter(article=article, user=request.user).first()  # sort obj LikeArticle ou None.

        # si l'user a deja un like , j'inverse le like sinon je créé un  nouvel obj:
        if 'like' in request.POST:
            # j'inverse le bool :
            if user_like_statut:
                user_like_statut.liked = not user_like_statut.liked
                user_like_statut.save()
            else:
                LikeArticle.objects.create(article=article, user=request.user, liked=True)

        # ici je check si y'a un 'next' dans le POST qui refere a l'url:
        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER', 'articles:feed')
        return redirect(next_url)
    
    # si jamais qq accede en GET:
    return redirect(request.META.get('HTTP_REFERER', 'articles:feed'))




    

