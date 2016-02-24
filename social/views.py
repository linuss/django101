from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse

# Create your views here.


def index(request):
    return render(request, 'social/index.html')


def login(request):
   user = authenticate(username=request.POST['username'], password=request.POST['password']) 
   if user is not None:
       return HttpResponseRedirect(reverse('social:home'))
   else:
       return HttpResponseBadRequest("The combination of username and password does not exist.")

def home(request):
    pass

           
