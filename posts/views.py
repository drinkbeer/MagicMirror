from django.shortcuts import render

from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Post
from .forms import PostForm

# Create your views here.
class HomePageView(ListView):
    model = Post
    template_name = 'home.html'

class CreatePostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post.html'
    success_url = reverse_lazy('home')

class SearchResultView(ListView):
    model = Post
    template_name = 'home.html'

    # Search results
    # queryset = Post.objects.filter(title__icontains='Winter') # new
    def get_queryset(self):
        query = self.request.GET.get('q')
        return Post.objects.filter(
            Q(title__icontains=query) | Q(detail__icontains=query)
        )
