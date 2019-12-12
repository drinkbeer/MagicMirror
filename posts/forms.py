from django import forms
from .models import Post

# Model for the form to submit images (products)
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'detail', 'cover']