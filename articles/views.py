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
    form = CommentForm()
    ctx: dict[str, Article] = {'articles':articles, 'form':form}
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
    
    # je check si un object like existe deja, sinon ca envoie None (.first()),
    # puis je vais chercher le statut du like si il existe:
    user_like_statut: LikeArticle = LikeArticle.objects.filter(user=request.user, article=article).first()


    form: CommentForm = CommentForm()
    # recuperation des commentaires de l'article:
    comments: List[Comment] = article.comment_set.all()

    ctx: Dict[str, Article | List[Comment] | CommentForm | LikeArticle] = {
        'article':article,
        'comments':comments,
        'form':form,
        'user_like_statut':user_like_statut,
        
        }
    
    return render(request, 'articles/article_detail.html', ctx)

          








    

