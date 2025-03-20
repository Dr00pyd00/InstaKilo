from django.shortcuts import render
from articles.models import Article
from django.http import HttpRequest, HttpResponse
from typing import Dict

# Create your views here.

def home(request: HttpRequest) -> HttpResponse:
    articles: Article = Article.objects.all()
    ctx: Dict[str, Article] = {'articles':articles}
    return render(request, 'main/home.html', ctx)