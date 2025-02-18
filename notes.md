# Django Notes

## Django Concepts

### Django Project vs. App

- Project: The overarching configuration and container for your entire web application.
  - Includes: settings, middleware, and database connections
- App: Modular component(s) with specific functionality. A project can have multiple apps

### MTV Architecture (Model-Template-View)

- Model: Represents the database schema and data handling. Each model is a Python class that maps to a database table
- Template: Handles the presentation layer, defined how data is displayed in HTML (or other formats)
- View: Contains the logic to process requests and return responses (rendering templates or returning JSON)

### Settings, URL and Routing

#### Settings

- `settings.py` contains global configurations (database connections, installed apps, middleware, templates, etc)
- Key settings:
  `INSTALLED_APPS`: active apps
  `DATABASES`: config for db connection
  `MIDDLEWARE`: middleware that handles requests/responses

#### URLS and Routing

- Django uses a URL dispatcher (`url.py`) to map URLS to views
- Project-level `urls.py` is the entry point for routing, while app-level `urls.py` organizes routes for individual apps

```py
# project/urls.py -> project level
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls'))
]

# blog/urls.py -> app level
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index')
]
```

### Models

- Django ORM (Object-Relational Mapping) allows us to define db schemas as Python classes

```py
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100) # short text
    content = models.TextField() # large text
    created_at = models.DateTimeField(auto_now_add=True) # date field
```

#### Database field types

##### Field Types for Data Representation

```py
    # text
    title = models.Charfield(max_length=255) # short text
    description = models.TextField() # long text

    # number
    age = models.IntegerField()
    price = models.FloatField()
    price_detailed = models.DecimalField(max_digits=10, decimal_places=2) # precise decimal numbers

    # boolean
    is_active = models.BooleanField(default=True)

    # date
    birth_rate = models.DateField() # data
    appointment_time = models.TimeField() # time
    created_at = models.DateTimeField() # data and time

    # file and image
    document = models.FileField(upload_to='documents/')
    profile_picture = models.ImageField(upload_to='images/')
```

##### Field Types for Relationships

```py
    author = models.Foreignkey(User, on_delete=models.CASCADE) # many to one
    profile = models.OneToOneField(User, on_delete=models.CASCADE) # one to one
    tags = models.ManyToManyField(Tag) # many to many
```

#### Other Fields

```py
# Specialized: choices, slug, email, url, uuid
# choices: predefined options, simular to enums
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published')

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, defaut='draft')
    slug = models.SlugField(unique=True)
    email = models.EmailField()
    website = models.URLField()
    identified = models.UUIDField(default=uuid.uuid4, editable=False)
]

# Auto
    id = models.AutoField(primary_key=True)

```

## Installation

- Since my Python environment is managed by Homebrew, I need to install it with a Virtual Environment

```zsh
python3 -m venv venv # create virtual env
source venv/bin/activate # activate the virtual env
pip install django

django-admin --version
```

## First Steps

```zsh
# Create Django project
django-admin startproject project_name

# Run the development server
# python path_to/manage.py runserver
python manage.py runserver # default path -> http://127.0.0.1:8000/

# Run migrations
python manage.py migrate

# Create an app
python manage.py startapp app_name
```

## Creating an App

- In Django a project is a collection of configurations and settings for your entire application, while an app is a modular component that performs a specific function or feature within the project
  - project
    - app 1
    - app 2
    - app 3

### Concepts

- Apps are self-container: Each app is designed to hanlde a specific functionality, such as managing users, blogs, e-commerce features, or API endpoints
- Reusable: they work across multiple Django projects. E.G.: You can create a "blog" app and reuse it in other projects with minimal modifications
- Separation of concerns: Apps help organize the code logically. Instead of having all models, views and templates in a single place, each app contains its own model, views and templates

#### Example

- E-commerce website project can be organized into apps, such as:
  - Users: Handles authentication, registration, and profile management
  - Products: Manages products listins, categories, and inventories
  - Orders: Deals with cart functionality, order creation and payments

```zsh
ptyhon manage.py startapp app_name
```

## Initial Project Folder Structure

```bash
project_name/ # root directory
├── manage.py # used for tasks such as running the server, creating apps, and applying migrations
├── project_name/
│   ├── __init__.py # it allows importing modules from thils folder
│   ├── asgi.py # async server gateway interface" entry point for async operations
│   ├── settings.py # contains all project-level config
│   ├── urls.py # maps urls to views
│   ├── wsgi.py # web server gateway interface: used to deploy dJANGO
└── db.sqlite3 (created after migrations)
```

## Creating an app

- Once our project is created, we can create an app with `python manage.py startapp app_name`
- Once that is done, we need to register the app on the project settings.py. settings.py > INSTALLED_APP > add app_name

```py
INSTALLED_APPS = [
    ...
    'django.contrib.staticfiles',
    "myapp" # we add the app(s) here
]
```

### Initial App Folder Structure

```bash
app_name/
├── admin.py # used to register models with Django's admin interface
├── apps.py # contains config for the app
├── migrations/ # tracks database schema changes
│   └── __init__.py
├── models.py # defines the app's db schema using Django ORM
├── tests.py
├── views.py # handles logic for responding to HTTP requests
├── __init__.py # marks the directory as Python package. Allows importing modules from this app.
├── urls.py # we create this one
```

### Connecting Views and Urls

```py
# project > app > views.py
from django.shortcuts import render, HttpResponse

def home(request):
    return HttpResponse("hello world")

===========

# project > app > urls.py
from django.urls import path
from . import views

urlpatterns = [
    #path(route, view, name)
    path("",views.home, name="home")
]
```

- After we set the views and the urls in the application-level, we need to set it also up on the project level

## Templates

- Reusable HTML file + dynamic data
- Create the templates inside the app_folder/templates
- Once we create our template, we should add them to view

```py
def home(request):
    # home.html is extending the content from base.html
    return render(request, 'home.html') # my_app/templates/home.html
```

## Database Models

- We create the models app/models.py as a Python class

```py
# app/models.py => create the models
from django.db import models

# Create your models here.
class TodoItem(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
```

- Once we create them, we register them on admin.py

```py
# app/admin.py => register the models
from django.contrib import admin
from .models import TodoItem

# Register your models here.
admin.site.register(TodoItem)
```

### Migrations

- When we make a change to our db models, we need to migrate. (Automated code which updates the db)
- Every time we make a change to the models, we run:
  - `python manage.py makemigrations`: creates the instructions to update the db
    - Create migration files based on models change.
    - Contains instructions on how to update the db schema
    - After we make changes to models
  - `python manage.py migrate`: applies the changes to db
    - Applies the migration files to the database
    - Updates the database

## Django Admin Panel

- Create a user: `python manage.py createsuperuser`
- Access the admin panel: `base-route/admin`
