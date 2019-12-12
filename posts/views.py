from django.shortcuts import render

from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse

from .models import Post
from .forms import PostForm
from .search import SearchForm
from .utils import get_top_n_similar

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
        ranked_img_paths = get_top_n_similar(images_dir='./media/images/*.jpg', 
                                              img_dir='./media', upload_img_path='./media/images/shirt0.png')
        return Post.objects.filter(
            Q(cover = ranked_img_paths[0])
        )

def search_by_image(request):

    print("Great! You successfully called method search_by_image")

    if request.method == 'POST':
        print("Great! You successfully submitted a POST request of your image")
        myimage = request.FILES['myimage']

        print(myimage.name)

        return HttpResponse("Image has been submitted successfully")

    return HttpResponse("Image has not been submitted")
    


