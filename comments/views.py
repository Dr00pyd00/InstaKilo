from django.shortcuts import render, redirect
from .models import Comment
from .forms import CommentForm
from django.http import JsonResponse
from django.views.generic import  DeleteView, UpdateView
from django.urls import reverse_lazy
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