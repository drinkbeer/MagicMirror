from django.urls import path
from django.conf.urls import url


from .views import HomePageView, CreatePostView, SearchResultView, search_by_image

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('post/', CreatePostView.as_view(), name='add_post'),
    path('search/', SearchResultView.as_view(), name='search_results'),
    url(r'^search_image/$', search_by_image, name='search_by_image'),
]