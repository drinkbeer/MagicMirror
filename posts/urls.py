from django.urls import path

from .views import HomePageView, CreatePostView, SearchResultView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('post/', CreatePostView.as_view(), name='add_post'),
    path('search/', SearchResultView.as_view(), name='search_results')
]