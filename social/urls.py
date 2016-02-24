from django.conf.urls import include, url
from social import views

urlpatterns = [
    url(r'$^',     views.index, name='index'),
    url(r'login/', views.login, name='login'),
]