from django.shortcuts import render

from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.db import models
from django.http import HttpResponse

from .models import Post
from .forms import PostForm
from .search import SearchForm
from .utils import get_top_n_similar

from django.core.files.storage import FileSystemStorage

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

def search_by_image(request):
    model = Post
    template_name = 'home.html'
    print("Great! You successfully called method search_by_image")

    if request.method == 'POST':
        print("Great! You successfully submitted a POST request of your image")
        myimage = request.FILES['myimage']

        print(myimage.name)
        fs = FileSystemStorage()
        filename = fs.save(myimage.name, myimage)
        uploaded_file_url = fs.url(filename)

        ranked_img_paths, indices = get_top_n_similar(images_dir='./media/images/*.jpg', 
                                              img_dir='./media', upload_img_path='.'+uploaded_file_url)
        print("temp file name: " + uploaded_file_url)

        obj_list = Post.objects.none()
        for index, rank_img_path in enumerate(ranked_img_paths[:3]):
            obj_list |= Post.objects.filter(Q(cover = rank_img_path))
        obj_list = obj_list.annotate(
                            search_type_ordering=models.Case(
                            models.When(Q(cover = ranked_img_paths[0]), then=models.Value(2)),
                            models.When(Q(cover = ranked_img_paths[1]), then=models.Value(1)),
                            models.When(Q(cover = ranked_img_paths[2]), then=models.Value(0)),
                            default=models.Value(-1),
                            output_field=models.IntegerField(),
                            )
                        ).order_by('-search_type_ordering')

        return render(request, 'home.html', {
            'object_list':obj_list
        })

    return HttpResponse("Image has not been submitted")
    