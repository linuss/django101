
# Django 101: Build a web-app in a day
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/florisdenhengst/django101?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Welcome to the Django 101: Build a web-app in a day tutorial! This git repository contains all the code you will have written yourself at the end of the day. The final result will be a small social network in which you can post statusses, pictures and comments.

To get started, please follow the instructions in this document. If you ever get stuck, you can check out the code in this repository, but try not to simply copy everything: you'll learn much more by writing it yourself. Each step will be explained here to guide you through the process.

# Prerequisites

In order to complete this tutorial, you'll need to have some stuff installed on your system. We'd like to refer you to the excellent [Installation chapter of Django for Girls] (http://tutorial.djangogirls.org/en/installation/index.html) (please don't feel offended if you're not a girl, we're pretty sure these instructions are unisex :))
If you get stuck somewhere along the line, don't hesitate to ask around in the 'Gitter' chat channel.

# Step 1
## Initializing the project
Django contains a lot of tools and commands that help you quickly create web-apps. To start our project off, in your terminal please type:
```bash
$ cd djangogirls/
$ source myvenv/bin/activate
(myvenv) $ django-admin startproject django101
(myvenv) $ pip install pillow
```

This should create a new django101 directory, which contains the basic necessities of a Django project.

Enter the directory and create your app by typing
```bash
(myvenv) $ cd django101
(myvenv) $ django-admin startapp social
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
     'social',
 ]
```

Then, create the initial database by typing
```bash
(myvenv) $ python3 manage.py migrate
```

This creates a set of default database tables that we're going to need later.

Finally, set up a superuser. This is necessary to be able to access the admin interface and create database entries for testing

```bash
(myvenv) $ python3 manage.py createsuperuser
```

You are now ready to start creating your app!

# Step 2
## Creating your database models

Most web-applications depend on data, which is stored in a database. Working with databases directly is often clunky however, so Django provides something called an ORM: an Object Relational Mapper. What this does is map regular Python classes to database tables, objects to database rows and functions to (parts of) SQL queries.

This might sound abstract, but follow along and it will become obvious soon. 

For our simple social network, we are going to need to store three things: Users, Posts and Comments. Fortunately, Users are provided automatically by Django (in the django.contrib.auth module), so we won't have to worry too much about them. Posts and Comments however, we'll need to create ourselves.

Let's create our models. Open the file `models.py` in the `django101/social` directory in your favorite editor, and edit it to contain the following:

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

You'll notice some properties have extra arguments. The ForeignKey argument determines to what other model this field refers. The `auto_now=True` argument for the DateTimeField makes sure that the current time is saved by default whenever a Post or Comment is added. The `null=True` and `blank=True` arguments for the ImageField specify that this is an optional field: you are allowed to create a post without an image.


To create the database tables, exit your editor and in the terminal go to the topmost django101 directory. There, type
```bash
(myvenv) $ python3 manage.py makemigrations social
(myvenv) $ python3 manage.py migrate
```

That's it! You now have the required database tables to build our web-app.
If you ever decide to make changes to these models, make sure to run `makemigrations` and `migrate` again!

# Step 3
## Create your first views and templates

In this step we will be creating our first views and templates. A view, which in most other MVC frameworks is called a Controller (confusing, we know...), is the code that is ran whenever you request a URL through your web browser. A view therefore must correspond with a url. 
The most common use case of a view is reading any potential parameters you send, retrieving some data from the database, and returning something that can be interpreted by your browser (often HTML or JSON). 

### Views
The first view we will be making is the index view. This is the view that gets called whenever you type in the address of your webapp in your browser. What we would like is to return an HTML page that contains a login form.

To do this, we must write the index view. Open `django101/social/views.py` and add the following lines:

```python
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'social/index.html')
```

As you can see, a view is nothing more than a Python function. A view always takes at least one parameter, the request object. This is something generated by Django that contains information about the request, such as which user made it and any parameters attached to the request. 

Because the index page of your webapp is a login page, nothing is yet known about visitors: the request object won't be of much use, so we won't do anything with it (yet). 

The index view returns the result of the render function (again provided by Django, as can be seen in the first line of the views file: `from django.shortcuts import render`). The render function takes two arguments: request, and the template we would like to return. We haven't created a template yet, but we'll get to that in a minute. For now, just fill in `"social/index.html"`.

### Templates

As mentioned earlier, a Django view will need to return something to display in the browser. For our index view, we'd like to return an HTML page that contains a login form. Instead returning a hand-wcrafted HTML file, we are going to use a template that from which an HTML file can be generated (or *rendered*). This makes it easier to adjust parts of the HTML file depending on the request, the number of users in the database or the time of the day.

A Django template is in many ways very similar to a regular HTML file. The difference is that you can add special Django-specific tags and keywords to help you. This is often useful to embed data retrieved from the database on the page you're returning. 

To create our first template issue the following command in the `django101/social` directory:
```bash
$ mkdir -p templates/social
```

The following directory structure should now exist: `django101/social/templates/social`. The double use of social seems unnecessary, but that's just how Django works (and there's probably a very good reason for it :)). By placing our templates in this directory, Django will automatically know where to find them (remember the render function call in the index view: all we gave as the template argument was `'social/index.html'`)

Now, in your editor, create a new file called `index.html` in the directory `django101/social/templates/social`. Type in the following content:
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
      <input required type="text" name="username" id="username-input">
      <label for="username-input">Username</label> <br />
      <input required type="password" name="password" id="password-input">
      <label for="password-input">Password</label> <br />
      <button type="submit"/>Log in</button>
    </form>
  </body>
</html>
```

This is a typical HTML file, save for the stuff in the `{% %}` brackets. These brackets tell Django that whenever it's rendering this file, it should do something special there.

You can ignore the `{% csrf_token %}` bit for now, this is some magic from Django that prevents CSRF (Cross-Site Request Forgery) attacks. The `"{% url 'social:login' %}"` bit is interesting tough.

If you didn't know, the HTML form `action` attribute describes what to do whenever a form is submitted. In regular HTML this attribute often contains the URL to which we want to send the filled in form. 
In our case, this is no different. However, instead of directly writing the URL, we're using Django tags to fill it in. This is better, because if we ever want to change the URL to which we want to send login forms, we don't have to adapt the template, just the urls-file (which we'll get to now). 

### URLs
As mentioned earlier, a view corresponds with a URL. Right now however, Django has no idea about any kinds of URLs, or how they are connected to views. Let's fix that.

In the directory `django101/django101`, you'll find a `urls.py` file. Open it in your editor, and edit it to look like this:

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

This file is used by Django to link URLs to views. URLs are matched by [regular expressions] (https://en.wikipedia.org/wiki/Regular_expression). We've added the line `url(r'^',       include('social.urls', namespace='social'))`. The first argument here is a regular expression that matches everything. The regular expression above it (`r'^admin/`) matches all URLs that end in `/admin`. It will send all these URLs to Django's admin module, because Django matches the URLs in this list from top to bottom.
We've specified here that any request will be routed through to our social app. However, we currently don't have any urls in our social app, so let's add them.

In the directory `django101/social` create a file `urls.py` and add the following content:
```
from django.conf.urls import include, url
from social import views

urlpatterns = [
    url(r'login/', views.social_login, name='login'),
    url(r'$^',     views.index, name='index'),
]
```

This `urls.py` file is very similar to the one in `django101/django101`. However, instead of redirecting the regular expressions to other `urls.py` files, we link them to our views! What happens here is that any request without anything behind it will be processed by the `index` view in `social/views.py`. The `index` view  is just a Python function which will be called whenever someone visits your web app landing page. Any request to URLs that end in `/login/` will be handled by a `social_login` view we have yet to write.

If you go back to our index.html template, we can see the `{% url social:login %}` tag. The part before the colon (:) specifies the namespace. We set the namespace in the `django101/django101/urls.py` file if you recall. The part after the colon specifies the name, which we just set in the `django101/social/urls.py` file. If we now wanted to change which view handles this login, all we'd have to do is change `views.login` to whatever new view we wrote. 

If you specifiy a view however, it must exist, and we don't have a login view yet! So, open up `social/views.py` again, and add the following 

```python
def social_login(request):
    pass
```

We'll implement this view in the next step. 

Now, to see if everything works, go to the top directory and type
```bash
(myvenv) $ python3 manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).
March 05, 2016 - 31:08:90
Django version 1.9, using settings 'django101.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

This starts the Django development server, so you can test your website! Open a browser and enter `localhost:8000` in the URL bar. You should be greated by our new site!

# Step 3
## Logging In

In the previous step, we created an empty login view. Let's flesh it out! 
In the `social_login` view, we'd like to authenticate the user. In our `index.html` template, we created a form that, when submitted, sends its data as POST-parameters to our login view ([w3schools.com](http://www.w3schools.com/tags/ref_httpmethods.asp) has a nice introduction to HTTP requests and parameters). This is where the `request` object that Django passes on to views comes into play. To access POST-parameters, in your view type `request.POST[<parameter_name>]`. The names of the parameters correspond to the name attributes on the inputs in your HTML form, so in our case 'username' and 'password'.

Open the `social/views.py` file and add the following:

```python
def social_login(request):
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
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.shortcuts import render
```

This view gets the submitted username and password from the POST parameters as submitted by the form. It then uses the Django built-in method `authenticate` to check whether this password-user combination is correct. If so, the user is returned (and so is not None). By then calling the login function, we make sure that the user is registered as being logged in. This means a cookie is returned to the user which will be used from now on to authenticate the user. 
We then return an `HttpResponseRedirect`, which redirects the user to the specified URL. `reverse` takes a url namespace and name (much like in our template), and converts it to an actual URL. This means that if a user succesfully logs in, (s)he will be redirected to the home page.

If however, the user cannot be authenticated, we return an `HttpResponseBadRequest` with a message. This message is shown whenever someone tries to log in but makes a mistake or does not exist.

Now that we've referred to the home url (in `reverse('social:home')`) we have to make sure it exists. In `social/views.py` add the following:

```python
def home(request):
    return HttpResponse('This is not the home page you are looking for.')
```

We'll also need to create a matching url. In `social/urls.py` add:
```python
    url(r'home/', views.home, name='home'),
```
to the `urlpatterns` list

That's it! We're now able to login to our webapp! There's nothing really to show yet, but we'll get to that next. Remember to try if everything works by going to the top `django101` directory and typing `(myvenv) $ python3 manage.py runserver`, and then browsing to `localhost:8000`. You can try logging in with the username and password you created in Step 1, and try logging in with a user that doesn't exist.

# Step 4
## Add home view and template

So, now that we've added a link to our home page, we should probably create a (real) view and a template for it too!
The home page will consist of a textbox in which the user can add a status. Below that we'll show a list of statuses (remind you of another website?). 

To do this, we'll first create the home template. Create the file `social/templates/social/home.html` and add the following content:

```html
<html>
  <head>
    <title> Social </title>
  </head>
  <body>
    <div id='new-post'>
      <h1> Write a new post </h1>
      <form action="{% url 'social:add_post' %}" method="post" id='new-post-form'>
      {% csrf_token %}
        <textarea name='text' form='new-post-form' required placeholder="Write your post here..."></textarea> 
        <input type='submit'/>
      </form>
    </div>


    {% for post in posts %}
    <div class='post' id="{{post.id}}">
      <p>{{post.text}}</p>
      <p>{{post.date_time}}</p>
    </div>
    {% endfor %}
  </body>
</html>
```

The top part of this template is very similar to the login page, so we won't discuss it. The bottom part is where the interesting stuff happens.
First the `{% for post in posts %}` tag. When our view is going to render this template later, the template will expect a `posts` parameter. In our template, we're going to loop over all elements in `posts`, and for each element, we'll create a `div`. Each `div` will contain two `<p>`paragraphs, the first containing the post's text, and the second the date and time at which the post was made. 
The `{{ }}` notation tells Django we'd like to show a variable. 

Now, we'll need to flesh out our home view. Open `social/views.py` and add the following:
```python
def home(request):
    posts = Post.objects.all()
    return render(request, 'social/home.html', {'posts': posts})

def add_post(request):
    pass
```

At the top, add the following import:
```python
from social.models import Post
```

This is the first time we're directly interacting with the database! Remember in step 1 where we declared our Post-model? By issuing the `Post.objects.all()` expression, we retrieve all the post objects in the database! Right now there aren't any, so the home page will be empty, but as soon as we've written the `add_post` view, we'll be able to see any statusses we've added.

Also, don't forget to add the URL in `social/urls.py`
```python
    url(r'post/add/', views.add_post, name="add_post"),
```
to the `urlpatterns` list.

### The Django Admin
Django comes with a very full-featured admin interface by default. This is useful for us now, so we can add posts before we've written a view that can do that for us. In order to make this possible, open the `admin.py` file in the `social` directory and add (note the import):

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

# Intermezzo -- Deploying!

This part of the workshop is placed here because it's probably a good idea to do it while there are other people around -- not because it is a logical next step in the tutorial.
It's all about making your creation available to the outside world by deploying it to some resource available to everyone.
You can skip it (for now) if you think it's not necessary or if you think you'll figure this out on your own, but we advise to do it while there are other people around since you have to be precise and since it's not really easy to debug stuff that's treated in this part.

## About deployment
Deploying your application is an important step: it makes your app available to anyone who's interested to join in on your awesome new and super-creative piece of work! Publishing work online is usually called 'deploying'. As the internet can be unsafe, there can be differences to a local version and an online version: the local version is usually called the 'development' version whereas the online version is called the 'production' version.

There are lots of ways to deploy a Django app and most of the trade-offs are really not that interesting until you know your specific use case: do you expect huge amounts of traffic? Do you want to use your own computer for hosting or is some online solution good enough? What's the budget?
Since most of these are not that relevant for this workshop, we'll proceed by deploying in a way that will probably fit everyone's 'requirements' for today: it shouldn't take too long and it should be free.

We'll start by introducing Git, which we'll use to share our code with the world (we're not that secretive about our code) and proceed by showing how to make your app itself accessible through PythonAnywhere.

But before we can start any of this, we have to update our ``settings.py`` file in the `django101/django101/` directory to be production-ready. Add the following line (at the bottom):
```python
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

## Git
Git is a very popular 'version control system'.
It tracks changes to files over time so that any version can be recalled later on.
The concept is comparable to "track changes" in Microsoft Word or the "Previous versions" feature of Dropbox, but it's way more refined and allows an amazing amount of control.

### Starting a repository
Git tracks changes to files in a specific directory (folder), which is called a code repository. Let's start one for our app!
Open a terminal in the topmost ``django101`` directory and run:
```bash
$ git init
$ git config --global user.name "Your Name"
$ git config --global user.email you@example.com
```

Git is now tracking the changes to all files in the topmost directory: you've succesfully created your first *repo* ;)
Since there will be some changes to the repository that are irrelevant, we proceed by telling Git which changes *not* to track: open a new file in your editor, add the following contents and save in the topmost ``django101`` directory with the name ``.gitignore``:
```
*.pyc
__pycache__
media
myvenv
db.sqlite3
/static
.DS_Store
```

Git will now ignore changes to these files. Changes to all other files will be tracked for you automatically. We'll look into how this is useful next.

### Adding stuff

After having 'initialized' the repository (whatever that may be), let's check out what Git thinks of our work so far:
```bash
$ git status
```
It should list all your files for this project as 'untracked' (except for everything in the `.gitignore` file).

We'll add all files and save our changes:
```bash
$ git add --all # this tells git that you want to add all changes it has found.
$ git commit -m "My awesome web-app, first commit" # this is the Git equivalent to saving your work.
```

### Publishing your code

[GitHub.com](https://www.github.com) is a place for storing and sharing code. Log in and create a new repository called 'django101'. Leave the "initialise with a README" checkbox unticked, leave the .gitignore option blank and leave License to None.

A screen will appear which shows your repo's clone URL. Switch to "HTTPS" and copy it. Open a terminal in the topmost ``django101`` directory and type:
```bash
# replace <your-github-username> with your actual username
$ git remote add origin https://github.com/<your-github-username>/django101.git
$ git push -u origin master
```

Enter your GitHub username and password when prompted and check out what happens: your code is now published to GitHub for the world to see!
You can check it out by browsing to [https://github.com/your-github-username/django101](https://github.com/<your-github-username>/django101) (replace with your github username ofcourse).

## PythonAnywhere
Now that we've shared our code with the world, it's time to make not only the *code*, but also the *actual app* available.

Browse to [PythonAnywhere.com](https://www.pythonanywhere.com) and log in. Choose the option "Bash" under "Start a new console". It's a way to access a terminal similar to the one you've been using today, except for that's it not on your computer but on a PythonAnywhere server. You can baffle your friends by telling you're creating an app 'in the cloud' ;)

### Getting the code on PythonAnywhere
To fetch the code from GitHub onto PythonAnywhere you can create a "clone" of the repo:
```bash
$ git clone https://github.com/<your-github-username>/django101.git
```

Now it's time to set up a virtualenv. This ensures that everything you install for your app is installed in *isolation* and won't affect any further projects you deploy on PythonAnywhere:
```
$ cd django101
$ virtualenv --python=python3.4 myvenv
$ source myvenv/bin/activate
(myvenv) $ pip install django==1.9 pillow # installs the packages on PythonAnywhere
(myvenv) $ python manage.py migrate # installs the database on PythonAnywhere
(myvenv) $ python manage.py createsuperuser # creates the user on PythonAnywhere
```

The final step in setting up a deployment is a new one. It is one of those things that is necessary in production because of the different requirements from development that you usually have when you're deploying.
It revolves around Django going through all apps with a vacuum cleaner in order to collect all static files and placing them in a single directory (the `STATIC_ROOT`).
This is convenient when you want to load the static files (images, css-files, javascript-files, etc.) through some high-performance static file server instead of a humble Python-based one.
In order to do this, type:
```bash
(myvenv) $ python manage.py collectstatic
```
Type `yes` when prompted. You'll see Django copying all kinds of static files (`.svg`, `.css`,
`.js`) from Django's admin module.

### Going live!
We've now got our code, dependencies and database on PythonAnywhere, so it's time to go live and conquer the world with our awesome social app!

Go back to the PythonAnywhere dashboard by clicking on its logo and go to the *Web* tab. Hit *Add a new web app*.

Confirm the domain name and select *manual configuration*. Make sure you don't select the "Django" option here!!! Next, choose Python3.4 and click Next to exit the wizard.

You are now in a PythonAnywhere config screen for your webapp. Go to the "Virtualenv" section, click the red text that says "Enter the path to a virtualenv" and enter `/home/<your-pythonanywhere-username>/django101/myvenv/`. Click the blue box with the check mark to save the path.

Now click the 'WSGI configuration file' link (in the "Code" section near the top of the page). Delete all contents and replace them with something like this (fill in your PythonAnywhere username):

```python
import os
import sys

path = '/home/<your-pythonanywhere-username>/django101'  # use your own username here
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'django101.settings'

from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler
application = StaticFilesHandler(get_wsgi_application())
```

This step is necessary to tell PythonAnywhere where the web app lives and how its Django setting file can be found (along with some other things).

Hit *Save* and then go back to the *Web* tab. Now hit the green reload button and browse to [https://your-pythonanywhere-username.pythonanywhere.com](https://your-pythonanywhere-username-.pythonanywhere.com) (replace with your own username ofcourse) and bask in your own awesomeness!

## Going live! ... again
Now that you've published *a* version of your app and feel like a minor god because of it, you probably want to do it any time you've added something cool to your web app.
This you can do by repeating these steps that were described above:
* On your computer:
	* `$ git status` to see what happened since your last commit
	* `$ git add --all` to notify git that you want to add all of your changes
	* `$ git commit -m "Some meaningful message"` to save your changes
	* `$ git push -u origin master` to publish your changes on GitHub
* On PythonAnywhere:
	* Log in and select 'Bash console 12345670' under *Your consoles*
  * (Optional) `$ cd django101` to move to the `django101` directory (when necessary)
  * (Optional) `$ source myvenv/bin/activate` activate your virtual environment (when necessary)
  * `(myvenv) $ git pull` to fetch the changes from GitHub
  * `(myvenv) $ python manage.py collectstatic` to copy your static files to the right place. Enter `yes` when prompted.
  * Click the PythonAnywhere logo, go to the "Web" tab and click "Reload".


# Step 5
## Add posts and comments

So now that we have the basics in place, lets implement the necessary functionality to post posts! We'll first write the view. Open `social/views.py` and add the following content:

```python
@login_required
def add_post(request)
    new_post = Post()
    new_post.text = request.POST['text']
    new_post.poster = request.user
    new_post.save()
    return HttpResponseRedirect(reverse('social:home'))
```

Alright, awesome! We can now save posts! However, this code isn't very safe: there's a few things that could go wrong here:
* This view might be called using a request that is not a POST-request (GET, PUT, UPDATE or DELETE). That's not allowed! For more info, check out [w3schools](http://www.w3schools.com/tags/ref_httpmethods.asp).
* The view might be called with a POST request, but not contain the 'text' key, which crashes our view!
* The `'text'` key might exist, but could contain an empty string! We don't want people being able to post empty statuses.

So, if any of these situations occurs, we'd like to return a `HttpResponseBadRequest`. However, all of the situations above could occur at any view that requires a post request and parameters. Therefore instead of writing some checks in every view, it's better to use a single function that checks everything:

```python
def _check_post_request(request, keys):
    # Check that the request method is POST
    if request.method != 'POST':
        return (False, "This method should be called with a POST method!")
    for key in keys:
        # Check that the key exists
        if key not in request.POST:
            return (False, "The POST request should contain a {} field".format(key))
        # Check that the text is not empty
        if not request.POST[key]:
            return (False, "The {} field cannot be empty!".format(key))

    return (True, "Everything is alright!")
```

This function takes a request object and a list of keys that are expected for this view. It then checks all the situations mentioned above. The function then returns a tuple with a boolean and a string. The boolean will be `False` if something is wrong, and `True` if everything checks out. The string describes what went wrong (or right). 

Now we can add it to `add_posts`:
```python
@login_required
def add_post(request):
    check = _check_post_request(request, ['text'])
    if check[0]:
        new_post = Post()
        new_post.text = request.POST['text']
        new_post.poster = request.user
        new_post.save()
        return HttpResponseRedirect(reverse('social:home'))
    else:
        return HttpResponseBadRequest(check[1])
```

We have another view that expects a POST request though: the `social_login` view! Let's add these checks there as well:

```python
def social_login(request):
   check = _check_post_request(request, ['username', 'password'])
   if check[0]:
       user = authenticate(username=request.POST['username'], password=request.POST['password']) 
       if user is not None:
           login(request, user)
           return HttpResponseRedirect(reverse('social:home'))
       else:
           return HttpResponseBadRequest("The combination of username and password does not exist.")
   else:
       return HttpResponseBadRequest(check[1])
```

While our own front-end should never get any of these wrong, it's never bad to expect the [worst] (https://en.wikipedia.org/wiki/Defensive_programming). Also, if we make an error when writing our front-end, we'll now catch the error and get a proper message to tell us what went wrong. 

Aside from Posts, we've also made room in our database for comments on these posts. We'll write the functionality for posting and displaying comments now too, as it's very similar to Posts.

In `home.html`, replace the part about posts with:

```html
{% for post in posts %}
<div class='post' id="{{post.id}}">
	<p>{{post.text}}</p>
	<p>{{post.date_time}}</p>
	<div class='comments'>
		<ul>
			{% for comment in post.comment_set.all %}
			<li> {{comment.text}} - {{comment.poster.username}} ({{comment.date_time | timesince}}) </li>
			{% endfor %}
		</ul>
	</div>
	<form action="{% url 'social:add_comment' %}" method="post">
	{% csrf_token %}
		<input type='text' name='comment' required placeholder="Write your comment here..."/>
		<input type='hidden' name='post_id' value={{post.id}} />
		<input type='submit'/>
	</form>
</div>
{% endfor %}
```

One thing that's new here is in the `{{comment.date_time | timesince}}` blob. The thing behind the pipe ('|') is called a filter. `timesince` is a Django built-in filter that converts a date and time to the amount of time that has passed since this date and time. 

As you might have guessed, we'll now need to add the `add_comment` view. Open `social/views.py` and add:

```python
from social.models import Comment, Post # put this at the top with the other imports

@login_required
def add_comment(request):
    check = _check_post_request(request, ['comment', 'post_id'])
    if check[0]:
        new_comment = Comment()
        new_comment.poster = request.user 
        new_comment.text = request.POST['comment']
        try:
            post = Post.objects.get(pk=request.POST['post_id'])
            new_comment.post = post
        except Post.DoesNotExist:
            return HttpResponseBadRequest("There is no Post with id {}".format(request.POST['post_id']))
        new_comment.save()
        return HttpResponseRedirect(reverse('social:home'))
    else:
        return HttpResponseBadRequest(check[1])
```

This view looks very similar to the `add_post` view, but there is one important difference: a comment always needs to be linked to a Post object. We're sending the ID of the post to which we want to attach a comment through the form, so we can look up the right post in our view. This is done in the line `post = Post.objects.get(pk=request.POST['post_id'])`. The `get()` function takes as argument a field and a value of the model on which it is called. In our case, we use `pk` which stands for Primary Key. 
The `get()` function will only succeed if there is only one model that corresponds to our arguments. We can be pretty sure there is only one Post with a certain ID, because this is enforced by the database. However, we could in theory try to save a comment on a post which does not exist. This is why the `get()` statement is wrapped in a `try` statement. If the operation fails, an `HttpResponseBadRequest` will be returned. 

We've got a new view, so don't forget to link it to a URL in `urls.py`:
```python
  urls(r'comment/add/', views.add_comment, name='add_comment')
```

At this point we have a basic functioning social network! Try posting some posts and comments and see how everything works :) Oh and in case you want to make another user so that you can socialize with yourself: you can easily do this via the Django's admin panel.
It looks kind of shabby though, so we'll add some formatting next.

# Step 6
## Layout and Formatting

We now have a working (albeit very basic) social network! However, it doesn't look like much yet, so we'll add some styling. If you are familiar with HTML and CSS, please feel free to use your own styling. 
Seeing as we are developers and not graphic designers, we've chosen to use all the help we could get and use [Bootstrap] (http://getbootstrap.com/), a CSS framework developed by Twitter. This allows us to very quickly style a page that looks presentable. Alternatives to Bootstrap are [Foundation] (http://foundation.zurb.com/), [Skeleton] (http://getskeleton.com/) and [Materialize] (http://materializecss.com/), but there are tons of others too.

To get started, in the`social` directory create a directory called `static`, which in turn contains a directory called `social`. In this directory, download the [latest version] (https://github.com/twbs/bootstrap/releases/download/v3.3.6/bootstrap-3.3.6-dist.zip) of Bootstrap and unzip it.

To load the static files into our HTML pages, first open `index.html` and change the `<head>` portion to look like this:
```html
<head>
  {% load staticfiles %}
  <title> Welcome to Social! </title>
  <link rel="stylesheet" href="{% static 'social/bootstrap-3.3.6-dist/css/bootstrap.css' %}"></link>
  <link rel="stylesheet" href="{% static 'social/bootstrap-3.3.6-dist/css/bootstrap-theme.css' %}"></link>
</head>
```

In order to get the most out of Bootstrap, you'll need to add some classes to your elements. Edit your `index.html` file to look like this:
```html
<html>
  <head>
    {% load staticfiles %}
    <title> Welcome to Social! </title>
    <link rel="stylesheet" href="{% static 'social/bootstrap-3.3.6-dist/css/bootstrap.css' %}"></link>
    <link rel="stylesheet" href="{% static 'social/bootstrap-3.3.6-dist/css/bootstrap-theme.css' %}"></link>
  </head>
  <body role='document'>
    <div class="container">
      <div class='jumbotron'>
        <h1> Welcome to Social, the least useful social network! </h1>
      </div>
      <div class='row'>
        <div class='col-xs-8 panel panel-default'>
          <div class='panel-body'>
            <p> Social is a minimalistic social network that allows you to share
            writings and pictures with the world. Don't bother with friends, share
            with everyone!
            </p>
          </div>
        </div>
        <div class='col-xs-4'>
          <h2> Please sign in to continue </h2>

          <form action="{% url 'social:login' %}" method="post">
            {% csrf_token %}
            <div class='form-group'>
              <label for="username-input">Username</label>
              <input type="text" class="form-control" required name="username" id="username-input"> 
            </div>
            <div class='form-group'>
              <label for="password-input">Password</label>
              <input type="password"  class="form-control"  required name="password" id="password-input"> 
            </div>
            <button type="submit" class="btn btn-primary">Log in</button>
          </form>
        </div>
      </div>
    </div>
  </body>
</html>
```

We'll do something very similar in `home.html`. Edit your file to look like this:
```html
<html>
  <head>
    {% load staticfiles %}
    <title> Social </title>
    <link rel="stylesheet" href="{% static 'social/bootstrap-3.3.6-dist/css/bootstrap.css' %}"></link>
    <link rel="stylesheet" href="{% static 'social/bootstrap-3.3.6-dist/css/bootstrap-theme.css' %}"></link>

  </head>
  <body>
    <div class='container'>

      <!-- New post container -->
      <div class='row'>
        <div class='col-xs-8 col-xs-offset-2'>
          <div class='panel panel-primary' id='new-post'>
            <div class='panel-body'>
              <h1> Write a new post </h1>
              <form action="{% url 'social:add_post' %}" method="post" id='new-post-form'>
              {% csrf_token %}
                <div class='form-group'>
                  <textarea class='form-control'name='text' form='new-post-form' required placeholder="Write your post here..."></textarea> 
                </div>
                <button type='submit' class='btn btn-default'>Post</button>
              </form>
            </div>
          </div>
        </div>
      </div>

      <!-- Previous posts container -->
      <div class='row'>
        <div class='col-xs-8 col-xs-offset-2'>
          {% for post in posts %}
          <div class='panel panel-default' id="{{post.id}}">
            <div class='panel-heading'>
              <h4>{{post.poster.username}}</h4>
              <h4 class='small'>posted on {{post.date_time}}</h4>
            </div>
            <div class='panel-body'>
              <p class='lead'>{{post.text}}</p>
            </div>
            <div class='row'>
              <div class='col-xs-10 col-xs-offset-1'>
                <ul class='list-group'>
                  {% for comment in post.comment_set.all %}
                  <li class='list-group-item'> 
                    {{comment.text}} - {{comment.poster.username}} ({{comment.date_time}}) 
                  </li>
                  {% endfor %}
                </ul>
                <form action="{% url 'social:add_comment' %}" method="post">
                {% csrf_token %}
                  <div class='form-group'>
                    <input class='form-control' type='text' name='comment' required placeholder="Write your comment here..."/>
                  </div>
                  <input type='hidden' name='post_id' value={{post.id}} />
                  <button class='btn btn-default' type='submit'>Submit</button>
                </form>
              </div>
            </div>
          </div>
          {% endfor %}
        </div>
      </div>
    </div>
  </body>
</html>
```

To check the results of your new stylings, make sure `$ python3 manage.py runserver` is (still) running, and open `localhost:8000` in your browser. That looks a lot better, right?!

# Step 7
## More database tricks

If you've played around with your new application you might have noticed something weird: the posts and comments are displayed in the wrong order! What we'd like ideally is if they were sorted on the time submitted, with the latest posts and comments ending up at the top. This is achieved fairly easily by using Django's awesome ORM. 

Open the `views.py` file, and change the line
```python
posts = Post.objects.all()
```
in the ``home`` function into
```python
posts = Post.objects.all().order_by('-date_time')
```

the `order_by()` function allows you to specify in which order you would like to retrieve your results from the database. It can take one or more arguments, which must be the names of the fields you'd like to order on (if you give it multiple field, it will order on the first field first, and then on the second). By prefixing the name of the field with a minus ('-') character, we indicate that we would like descending order, instead of the default ascending order. 
As an example, you could try ordering your post by username like this `Post.objects.order_by('poster__username')`. 

We probably want the same thing for our comments. Because we are using the Django Template language to access our comments, this is slightly more difficult. The easiest way to solve this is to give the `Comment` class a default ordering. This makes sense, as we'll probably want to order our comments by time posted throughout our entire app anyways. 

To accomplish this, open the `models.py` file and add the following:


```python
class Comment(models.Model):
    ...
    class Meta:
        ordering = ['-date_time']
```

This makes sure that whenever you're requesting comments from the database, the latest comment is returned first.

## Uploading photos
If you recall, when we created our models we added a `photo` field to the `Post` class. It's time we use it!

To get uploading photos to work, we'll need to lay a little bit of a foundation. First, open `django101/django101/settings.py` and add the following lines:

```python

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'
```

This tells Django where to store any uploaded images, and where to find them if they're to be displayed on a page.

Then, open `django101/django101/urls.py` and add the following imports:
```python
from django.conf import settings
from django.conf.urls.static import static
```
and edit `urlpatterns` so it looks like this:
```python
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^',       include('social.urls', namespace='social')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

After doing this, we'll need to add the file upload dialog to the post-creator form. Open `home.html` and edit the post form to look like this:
```html
<!-- New post container -->
<div class='row'>
  <div class='col-xs-8 col-xs-offset-2'>
    <div class='panel panel-primary' id='new-post'>
      <div class='panel-body'>
        <h1> Write a new post </h1>
        <form action="{% url 'social:add_post' %}" method="post" id='new-post-form' enctype='multipart/form-data'>
        {% csrf_token %}
          <div class='form-group'>
            <textarea class='form-control'name='text' form='new-post-form' required placeholder="Write your post here..."></textarea> 
          </div>
          <div class='form-group'>
            <input id='photo-upload' class='form-control' 
                   type='file' name='photo' accept='image/*'>
            </input>
            <label for='photo-upload'>Upload a photo</label>
          </div>
          <button type='submit' class='btn btn-default'>Post</button>
        </form>
      </div>
    </div>
  </div>
</div>
```
Pay attention to the extra attribute `enctype` added to the opening `<form>` tag. This is necessary if you want to send more than plain text. 

Now, we don't just want to upload photos, we'd like to show them too! Add the following bit:
```html
...
<div class='panel-body'>
  <p class='lead'>{{post.text}}</p>
</div>
{% if post.photo %}
<div class='col-xs-10 col-xs-offset-1'>
  <img class='img-responsive center-block img-rounded' src={{post.photo.url}}/>
</div>
{% endif %}
...
```

Bear in mind that if you chose to do your own styling in the previous step, you can leave out the HTML classes and substitute your own.

Finally, we'll need to make sure that any photo that gets sent is stored! Open up `views.py` and add the following lines:
```python
...
def add_post(request):
new_post.poster = request.user
if 'photo' in request.FILES and request.FILES['photo'] is not None:
    new_post.photo = request.FILES['photo']
new_post.save()
...
```

That's it! You can now upload and view photos! 

## Searching for posts

Let's implement a little bit of search functionality! This will show some handy aspects of the Django ORM.

First, we'll create a search box. Open up `home.html`, and edit the `New post container` to look like this:
```html
<div class='row'>
  <!-- New post container -->
  <div class='col-xs-8 col-xs-offset-2'>
    <div class='panel panel-primary' id='new-post'>
      <div class='panel-body'>
        <h1> Write a new post </h1>
        <form action="{% url 'social:add_post' %}" method="post" id='new-post-form' enctype='multipart/form-data'>
        {% csrf_token %}
          <div class='form-group'>
            <textarea class='form-control'name='text' form='new-post-form' required placeholder="Write your post here..."></textarea> 
          </div>
          <div class='form-group'>
            <input id='photo-upload' class='form-control' 
                   type='file' name='photo' accept='image/*'>
            </input>
            <label for='photo-upload'>Upload a photo</label>
          </div>
          <button type='submit' class='btn btn-default'>Post</button>
        </form>
      </div>
    </div>
  </div>

  <!-- Search box -->
  <div class='col-xs-2'>
    <div class='well'>
      <form action="{% url 'social:home' %}" method="post" id='search-bar'>
        {% csrf_token %}
        <div class='form-group'>
          <input type='text' class='form-control' name='search_terms' required placeholder='Search in posts...'>
        </div>
        <button type='submit' class='btn btn-primary'>Search</button>
      </form>
      <a class='btn btn-success' href="{% url 'social:home' %}">Show all</a>
    </div>
  </div>
</div>
```

Notice that we've created a button and a link: the button will, just like all previous forms, send your parameters to the backend. The link will just return you to the default home page. 

Now, we'll need to adapt the home view so it can deal with any search parameters. Open `views.py` and edit `home` to look like this:
```python
@login_required
def home(request):
    if request.method == 'GET':
        posts = Post.objects.all()
    elif request.method == 'POST':
        check = _check_post_request(request, ['search_terms'])
        if check[0]:
            search_term = request.POST['search_terms']
            posts = Post.objects.filter(text__icontains=search_term).
        else:
            return HttpResponseBadRequest(check[1])
    posts = posts.order_by('-date_time')
    return render(request, 'social/home.html', {'posts': posts})
```
As you can see, the home view can now deal with two kinds of requests: regular GET requests and POST requests.
Just like our other post requests, we start with checking if everything is in order. Then, once we've gotten the search parameters from the request, we get our Post objects, but with a condition: the post text must contain the search terms. 
This introduces another important part of the Django ORM: `filter()`. Filtering results from a database is a very common operation. In this case, we're looking for any posts which texts contain our search terms. If we would like to match text completely, we could write `filter(text=<our search term>)`. The filter method can be used on any of the fields in our model. For example, say we'd only want comments posted in 2016, we could do something like:
```python

import datetime

cutoff = datetime.datetime(year=2016)
comments = Comment.objects.filter(date_time__gt=cutoff)
```
Et voila! (Note: the `__gt` bit means Greater Than). 

## Deleting post
Now that you've been playing around with your app for a while, you'll probably notice the home page flooding with nonsense test posts. Wouldn't it be great if we could remove some of them? 
However, we have to make sure that we're the only ones that can remove our posts: it would be weird if you could delete everything your friends have written!

To accomplish this, let's first create a delete button in the template.
Open `home.html` and make it look like this (you have to replace the panel-header part):

```html
<div class='panel-heading'>
  <h4>{{post.poster.username}}</h4>
  <h4 class='small'>
    posted on {{post.date_time}}
    {% if post.poster == user %}
    <form action="{% url 'social:delete_post' post.id %}" method="post" id='delete-post'>
      {% csrf_token %}
      <button type='submit'title='delete post' class='glyphicon glyphicon-trash pull-right'></button>
    </form>
    {% endif %}
  </h4>
</div>
```

Note that the delete icon is part of Bootstrap. If you've chosen your own formatting, you could save your own icon in the `social/static` directory and refer to it like `<img src="{% static 'social/images/<img_name>' %}"/>`. 
What's new here is the use of the `{% if %}` tag. The if-tag makes sure everything in it is only shown if the condition in the tag is true, or the object mentioned actually exists. In this case, we're only showing the delete button on posts that are actually yours! We do need to supply the template with an extra argument though, `user`. Let's do that first. In `views.py` add:

```python
return render(request, 'social/home.html', {'posts': posts, 'user': request.user})
```

Okay, now that that's taken care off, we'll need to write a new view that delete's a post. In `views.py` add the following:
```python
@login_required
def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user != post.poster:
        return HttpResponseForbidden("You can only delete your own posts!")
    else:
        post.delete()
        return HttpResponseRedirect(reverse('social:home'))
```

We're using two new things here: the `delete()` method, and the `HttpResponseForbidden`. The delete method, when called on a database object, deletes that object from the database (duh..). The `HttpResponseForbidden` is returned whenever you're trying to delete someone else's post (even though you can't see the delete button, you could still access the underlying URL). 
Make sure to add `HttpResponseForbidden` to your imports!
```python
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
```

Finally, we'll need to add a url. However, as you can see in the view, the `delete_post` method gets an extra parameter: `post_id`. This is how to do that:
```python
url(r'post/delete/(?P<post_id>[0-9]+)/$',   views.delete_post, name="delete_post"),
```
Add this line to the `urlpatterns` in `social/urls.py`. The `(?P<post_id>[0-9]+)` ties a parameter name to a regular expression. In this case, the regular expression matches one or more digits between 0 and 9: the post id. To delete a post, simply visit the url `/post/delete/<post_id>`!

Since the delete button we've just added is linked to this url, you should now be able to delete your test posts and clean up your home page!

# Step 8
## Your turn!

You know have a pretty cool basic social web-app! This is also the end of the tutorial. However, there are a lot more features that could make this app even cooler! Here's a list of things we could think of:
* Create a profile page that lists details about a user
* Make comments deletable too
* Support 'Friendships': link users together, and only show posts made by friends on their home page
* Create a 'Like' and 'Dislike' button on posts or comments
* Comment on comments!
* Create a signup page where new member can register

We'll be around to help if you'd like to create any of these features, or any that you can think of yourselves!

We hope you enjoyed this tutorial!
















