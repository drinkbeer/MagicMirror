from django import forms
from .models import Post

# Model for Search Image result
class SearchForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['cover']