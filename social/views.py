from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from social.models import Post

# Create your views here.


def index(request):
    return render(request, 'social/index.html')


def login(request):
   user = authenticate(username=request.POST['username'], password=request.POST['password']) 
   if user is not None:
       return HttpResponseRedirect(reverse('social:home'))
   else:
       return HttpResponseBadRequest("The combination of username and password does not exist.")

@login_required
def home(request):
    posts = Post.objects.all()
    return render(request, 'social/home.html', {'posts': posts})

def add_post(request):
    pass
           
