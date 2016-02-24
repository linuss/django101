from django.conf.urls import url
from social import views

urlpatterns = [
    url(r'$^',           views.index, name='index'),
    url(r'login/',       views.login, name='login'),
    url(r'home/',        views.home, name='home'),
    url(r'post/add/',    views.add_post, name="add_post"),
    url(r'comment/add/', views.add_comment, name="add_comment"),
]
