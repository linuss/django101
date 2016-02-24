# Django 101: Build a web-app in a day

Welcome to the Django 101: Build a web-app in a day tutorial! This git repository contains all the code you will have written yourself at the end of the day. The final result will be a small social network in which you can post statusses, pictures and comments.

To get started, please follow the instructions in this document. If you ever get stuck, you can check out the code in this repository, but try not to simply copy everything: you'll learn much more by writing it yourself. Each step will be explained here to guide you through the process.

# Prerequisites

In order to complete this tutorial, you'll need to have some stuff installed on your system. We'd like to refer you to the excellent [Installation chapter of Django for Girls] (http://tutorial.djangogirls.org/en/installation/index.html) (please don't feel offended if you're not a girl, we're pretty sure these instructions are unisex :))

# Step 1
## Initializing the project

Django contains a lot of tools and commands that help you quickly create web-apps. To start our project off, in your terminal please type
```
django-admin startproject django101
```

This should create a django101 directory, which contains the basic necessities of a Django project.

Enter the directory and create your app by typing
```
cd django101
django-admin startapp social
```

We must also make Django aware of our new app. To do so, add `social` to the `INSTALLED_APPS` list in django101/settings.py.
Do so by opening this file in your favorite editor and adding it. The final result should look like:
```
 INSTALLED_APPS = [
     'django.contrib.admin',
     'django.contrib.auth',
     'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
     'social'
 ]
```

Then, create the initial database by typing
```
python3 manage.py migrate
```

This creates a set of default database tables that we're going to need later.

Finally, set up a superuser. This is necessary to be able to access the admin interface and create database entries for testing

```
python3 manage.py createsuperuser
```

You are now ready to start creating your app!

# Step 2
## Creating your database models

Most web-applications depend on data, which is stored in a database. Working with databases directly is often clunky however, so Django provides something called an ORM: an Object Relational Mapper. What this does is map regular Python classes to database tables, and objects to database rows. 

This might sound abstract, but follow along and it will become obvious soon. 

For our simple social network, we are going to need to store three things: Users, Posts and Comments. Fortunately, Users are provided automatically by Django (in the django.contrib.auth module), so we won't have to worry too much about them. Posts and Comments however, we'll need to create ourselves.

Let's create our models. Open the file models.py in the django101/social directory in your favorite editor, and edit it to contain the following:

```python
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    text = models.TextField()
    poster = models.ForeignKey(User)
    date_time = models.DateTimeField(auto_now=True)
    photo = models.ImageField(null=True, blank=True)

class Comment(models.Model):
    text = models.TextField()
    poster = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    date_time = models.DateTimeField(auto_now=True)   
```

These classes will be read by Django and transformed into database tables. Both tables will have four columns, one for each property we have specified above. 
The type of the property (TextField, ForeignKey etc.) specifies to Django what kind of columns to create in the database.
You'll notice some properties have extra arguments. The ForeignKey argument determines to what other model this field refers. The auto_now=True argument for the DateTimeField makes sure that the current time is saved by default whenever a Post or Comment is added. The null=True and blank=True arguments for the ImageField specify that this is an optional field: you are allowed to create a post without an image.


To create the database tables, exit your editor and in the terminal go to the topmost django101 directory. There, type
```
python3 manage.py makemigrations social
python3 manage.py migrate
```

That's it! You now have the required database tables to build our web-app.
If you ever decide to make changes to these models, make sure to run `makemigrations` and `migrate` again!

# Step 2
## Create your first views and templates

In this step we will be creating our first views and templates. A view, which in most other MVC frameworks is called a Controller (confusing, we know...), is the code that is ran whenever you request a URL through your web browser. A view therefore must correspond with a url. 
The most common use case of a view is reading any potential parameters you send, retrieving some data from the database, and returning something that can be interpreted by your browser (often HTML or JSON). 

### Views
The first view we will be making is the index view. This is the view that gets called whenever you type in the address of your webapp in your browser. What we would like is to return an HTML page that contains a login form.

To do this, we must write the index view. Open `django101/social/views.py` and add the following lines:

```python
def index(request):
    return render(request, 'social/index.html')
```

As you can see, a view is nothing more than a Python function. A view always takes at least one parameter, the request object. This is something generated by Django that contains information about the request, such as which user made it and any parameters attached to the request. 

Seeing as when you access the index page of your webapp nothing is yet known about you, the request object won't be of much use, so we won't do anything with it (yet). 

The index view returns the result of the render function (again provided by Django, as can be seen in the first line of the views file: `from django.shortcuts import render`). The render function takes two arguments: request, and the template we would like to return. We haven't created a template yet, but we'll get to that in a minute. For now, just fill in `"social/index.html"`.

### Templates

As mentioned earlier, a Django view will need to return something to display in the browser. For our index view, we'd like to return an HTML page that contains a login form. However, instead of simply returning an HTML file, we are going to return a template.

A Django template file is in many ways very similar to a regular HTML page. The difference is that you can add special Django-specific tags and keywords to help you. This is often useful to embed data retrieved from the database on the page you're returning. 

Now, to create our first template. In the social directory, issue the following commands:
```
mkdir -p templates/social
```

The following directory structure should now exist: `django101/social/templates/social`. The double use of social seems unnecessary, but that's just how Django works (and there's probably a very good reason for it :)). By placing our templates in this directory, Django will automatically know where to find them (remember the render function call in the index view: all we gave as the template argument was `'social/index.html'`)

Now, in your editor, create a new file called index.html in the directory `social/templates/social. Type in the following content:
```html
<html>
  <head>
    <title> Welcome to Social! </title>
  </head>
  <body>
    <h1> Welcome to Social, the least useful social network! </h1>
    <h2> Please sign in to continue </h2>

    <form action="{% url 'social:login' %}" method="post">
      {% csrf_token %}
      <input type="text" name="username" id="username-input">
      <label for="username-input">Username</label> <br />
      <input type="password" name="password" id="password-input">
      <label for="password-input">Password</label> <br />
    <input type="submit"/>
    </form>
  </body>
</html>
```

This is a typical HTML file, save for the stuff in the `{% %}` brackets. These brackets tell Django that whenever we're rendering this file, it should do something special here.

You can ignore the `{% csrf_token %}` bit for now, this is some magic from Django that prevents CSRF (Cross-Site Request Forgery) attacks. The `"{% url 'social:login' %}"` bit is interesting tough.

If you didn't know, the HTML form action attribute describes what to do whenever a form is submitted. In regular HTML this attribute often contains the URL to which we want to send the filled in form. 
In our case, this is no different. However, instead of directly writing the URL, we're using Django tags to fill it in. This is better, because if we ever want to change the URL to which we want to send login forms, we don't have to adapt the template, just the urls-file (which we'll get to now). 

### URLs
As mentioned earlier, a view corresponds with a URL. Right now however, Django has no idea about any kinds of URLs, or how they are connected to views. Let's fix that.

In the directory `django101/django101`, you'll find a urls.py file. Open it in your editor, and edit it to look like this:

```python
from django.conf.urls import url, include
from django.contrib import admin
import social

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^',       include('social.urls', namespace='social')),
]      
```
(You can leave the comments at the top or remove them, whatever you like).
Note that we've added `include` to the first line. 

This file is used by Django to link URLs to views. URLs are matched by [regular expressions] (https://en.wikipedia.org/wiki/Regular_expression). We've added the line `url(r'^',       include('social.urls', namespace='social'))`. The first argument here is a regular expression that matches everything. However, because of the regular expression above it (`r'^admin/`), URLs that end in /admin will be handled by the admin module (provided by Django).
We've specified here that any request will be routed through to our social app. However, we currently don't have any urls in our social app, so let's add them.

In the directory `django101/social` create a file `urls.py` and add the following content:
```
from django.conf.urls import include, url
from social import views

urlpatterns = [
    url(r'$^',     views.index, name='index'),
    url(r'login/', views.social_login, name='login'),
]   
```

This file is very similar to the one in `django101/django101`. However, instead of redirecting the regular expressions to other url-files, we link them to our views! What happens here is that any request without anything behind it will be processed by the index view (or method) in `social/views.py`. Any request that ends in `/login/` will be handled by a social_login view we have yet to write.

If you go back to our index.html template, we can see the `{% url social:login %}` tag. The part before the colon (:) specifies the namespace. We set the namespace in the `django101/django101/urls.py` file if you recall. The part after the colon specifies the name, which we just set in the `django101/social/urls.py` file. If we now wanted to change which view handles this login, all we'd have to do is change `views.login` to whatever new view we wrote. 

If you specifiy a view however, it must exist, and we don't have a login view yet! So, open up `social/views.py` again, and add the following 

```python
def social_login(request):
    pass
```

We'll implement this view in the next step. 

Now, to see if everything works, go to the top directory and type `python3 manage.py runserver`. This starts the Django development server, so you can test your website! Open a browser and enter `localhost:8000` in the URL bar. You should be greated by our new site!

# Step 3
## Logging In

In the previous step, we created a shim login view. Let's flesh it out! 
In the social_login view, we'd like to authenticate the user. In our index.html template, we created a form that, when submitted, sends its data as POST-parameters to our login view. This is where the request object comes in. To access POST-parameters, in your view type `request.POST[<parameter_name>]`. The names of the parameters correspond to the name attributes on the inputs in your HTML form, so in our case 'username' and 'password'.

Open the `social/views.py` file and add the following:

```python
def login(request):
   user = authenticate(username=request.POST['username'], password=request.POST['password']) 
   if user is not None:
       login(request, user)
       return HttpResponseRedirect(reverse('social:home'))
   else:
       return HttpResponseBadRequest("The combination of username and password does not exist.")
```

At the top of your file, make sure we have the necessary imports:

```python
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse
```

This view gets the submitted username and password from the POST parameters as submitted by the form. It then uses the Django built-in method 'authenticate' to check whether this user exists. If so, the user is returned (and so is not None). By then calling the login function, we make sure that the user is registered as being logged in. This means a cookie is returned to the user which will be used from now on to authenticate the user. 
We then return an `HttpResponseRedirect`, which redirects the user to the specified URL. `reverse` takes a url namespace and name (much like in our template), and converts it to an actual URL. This means that if a user succesfully logs in, (s)he will be redirected to the home page.

If however, the user cannot be authenticated, we return an `HttpResponseBadRequest` with a message. This message is shown whenever someone tries to log in but makes a mistake or does not exist.

Now that we've referred to the home url (in `reverse('social:home')`) we have to make sure it exists. In `social/views.py` add the following:

```python
def home(request):
    pass
```

We'll also need to create a matching url. In `social/urls.py` add:
```python
url(r'home/', views.home, name='home'),
```
to the `urlpatterns` list

That's it! We're now able to login to our webapp! There's nothing really to show yet, but we'll get to that next. Remember to try if everything works by going to the top directory and typing `python3 manage.py runserver`, and then browsing to `localhost:8000`. You can try logging in with the username and password you created in step 1, and try logging in with a user that doesn't exist.

# Step 4
## Add home view and template

So, now that we've added a link to our home page, we should probably create a (real) view and a template for it too!
The home page will consist of a textbox in which the user can add a status. Below that we'll show a list of statusses (remind you of another website?). 

To do this, we'll first create the home template. Create the file `social/templates/social/home.html` and add the following content:

```html
<html>
  <head>
    <title> Social </title>
  </head>
  <body>
    <div id='new-post'>
      <h1> Write a new post <h1>
      <form action="{% url 'social:add_post' %}" method="post" id='new-post-form'>
      {% csrf_token %}
        <textarea name='text' form='new-post-form' placeholder="Write your post here..."></textarea> 
        <input type='submit'/>
      </form>
    </div>


    {% for post in posts %}
    <div class='post' id="{{post.id}}">
      <p>{{post.text}}<p>
      <p>{{post.date_time}}</p>
    </div>
    {% endfor %}
  </body>
</html>
```

The top part of this template is very similar to the login page, so we won't discuss it. The bottom part is where the interesting stuff happens.
First the `{% for post in posts %}` tag. When our view is going to render this template later, the template will expect a `posts` parameter. In our template, we're going to loop over all elements in `posts`, and for each element, we'll create a `div`. Each `div` will contain two paragraphs, the first containing the post's text, and the second the date and time at which the post was made. 
The `{{ }}` notation tells Django we'd like to show a variable. 

Now, we'll need to flesh out our home view. Open `social/views.py` and add the following:
```python
def home(request):
    posts = Post.objects.all()
    return render(request, 'social/home.html', {'posts': posts})

def add_posts(request):
    pass
```

At the top, add the following import:
```python
from social.models import Post
```

This is the first time we're directly interacting with the database! Remember in step 1 where we declared our Post-model? By issuing the `Post.objects.all()` expression, we retrieve all the post objects in the database! Right now there aren't any, so the home page will be empty, but as soon as we've written the `add_post` view, we'll be able to see any statusses we've added.

Also, don't forget to add the URL in `social/urls.py`
```python
url(r'post/add/', views.add_post, name="add_post")
```
to the `urlpatterns` list.

### The Django Admin
Django comes with a very full-featured admin interface by default. This is useful for us now, so we can add posts before we've written a view that can do that for us. In order to make this possible, open the `admin.py` file in the `social` directory and add:

```python
from social.models import *

admin.site.register(Post)
admin.site.register(Comment)
```

This tells the Admin module to create admin interfaces for the Post and Comment models we've created. To see this in action, make sure the `runserver` command is still running, or start it up again, and in your browser go to `localhost:8000/admin`. You can log in with the same username as on your regular site.

On this screen you can edit the database for all registered models. Try creating a new Post, and then view your home page again. It should show up!

There's one last thing we need to do before moving on. Remember how we wrote that great login page? Right now, it's pretty useless: try clearing your cache or opening up an Incognito window and surfing to `localhost:8000/home`. You should still be able to view all the posts! 
This is obviously not what we want, so we should make sure that the home view only returns the template if it is requested by a logged-in user. We could do this in much the same way as in login view (using the `authenticated` method, but we're probably going to want to check this for a lot of views. 
Django has a more elegant solution though! Add the following to your `social/views.py` imports:
```python
from django.contrib.auth.decorators import login_required
```
and then above your home view add `@login_required`, so the whole view looks like this:

```python
@login_required
def home(request):
    posts = Post.objects.all()
    return render(request, 'social/home.html', {'posts': posts})

```

Then, to the file `django101/django101/settings.py` add the following (at the bottom):
```python
LOGIN_URL = '/'
```

Now try to view `localhost:8000/home` again in an Incognito window. Instead of showing the posts, you should be redirected to the regular index page which asks for your username and password!












