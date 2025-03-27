from django.shortcuts import render
from articles.models import Article
from django.http import HttpRequest, HttpResponse
from typing import Dict
from comments.forms import CommentForm
# Create your views here.

def home(request: HttpRequest) -> HttpResponse:
    articles: Article = Article.objects.all()
    form = CommentForm()
    ctx: Dict[str, Article] = {'articles':articles, 'form':form}
    return render(request, 'main/home.html', ctx)