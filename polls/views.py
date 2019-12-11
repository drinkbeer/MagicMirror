from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, World. This is the first page of Magic Mirror!")