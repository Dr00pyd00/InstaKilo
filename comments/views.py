from django.shortcuts import render, redirect
from .models import Comment
from .forms import CommentForm
from django.http import JsonResponse
from django.views.generic import  DeleteView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from articles.models import Article
# Create your views here.



 # je fais une classView pour editer un commentaire:
class CommentDelete(DeleteView):
    model = Comment
    template_name = 'comments/delete_comment.html'

    def get_success_url(self):
        return reverse_lazy('articles:detail', kwargs={'pk': self.object.article.pk})
    

class CommentEdit(UpdateView):
    model = Comment
    template_name = 'comments/edit_comment.html'
    fields = ['text']

    def get_success_url(self):
        return reverse_lazy('articles:detail', kwargs={'pk': self.object.article.pk})
    
def post_a_comment(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        print('ca passe ici')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.article = article
            comment.save()
    return redirect(request.META.get('HTTP_REFERER', 'articles:index'))  