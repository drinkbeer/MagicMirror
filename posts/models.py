from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=400)
    detail = models.TextField()
    cover = models.ImageField(upload_to='images/')
    link = models.URLField(max_length=300, default='https://www.shopify.com/')
    store = models.CharField(max_length=100, default='Shopify')

    def __str__(self):
        return self.title
