# Django Rest Framework

### Table of contents

1. [Setup](#1-setup)
   - 1.1. [Setup a virtual environment](#11-setup-a-virtual-environment)
   - 1.2. [Create `requirements.txt` + installation](#12-create-requirementstxt--installation)
   - 1.3. [Create django project and an app](#13-create-django-project-and-an-app)
   - 1.4. [Add installed apps](#14-add-installed-apps)
2. [Generating API](#2-generating-api)
   - 2.1. [Create a model](#21-create-model)
   - 2.2. [Create a serializer](#22-create-serializer)
   - 2.3. [Create a view](#23-create-a-view)
   - 2.4. [Config URLs](#24-config-urls)
   - 2.5. [Registering models in the admin panel](#25-registering-models-in-the-admin-panel)
   - 2.6. [Running the server](#25-running-the-server)
3. [Dockerizing the project](#3-dockerizing-the-project)
   - 3.1. [Create a Dockerfile](#31-create-a-dockerfile)
   - 3.2. [Create a docker-compose file](#32-create-a-docker-compose-file)
   - 3.3. [Build and run the container](#33-build-and-run-the-container)
4. [Types of views](#4-types-of-views)
   - 4.1. [Function-based views](#41-function-based-views)
   - 4.2. [Class-based views](#42-class-based-views)
   - 4.3. [Viewsets](#43-viewsets)
   - 4.4. [Generic views](#44-generic-views)
   - 4.5. [Mixins](#45-mixins)
     -4.6. [APIView](#46-apiview)

<a name="1-setup"></a>

## 1. Setup

<a name="11-setup-a-virtual-environment"></a>

### 1.1. Setup a virtual environment

```bash
mkdir drf_project && cd drf_project
python3 -m venv venv
source venv/bin/activate
```

<a name="12-create-requirementstxt--installation"></a>

### 1.2. Create `requirements.txt` + installation

```txt
django
djangorestframework
```

```bash
pip3 install -r requirements.txt
```

<a name="13-create-django-project-and-an-app"></a>

### 1.3. Create django project and an app

```bash
django-admin startproject [django-project] .
python manage.py startapp api
```

<a name="14-add-installed-apps"></a>

### 1.4. Add installed apps

```py
# [django-project]/settings.py

INSTALLED_APPS = [
    ...

    # Third-party apps
    'rest_framework',

    # Local apps
    'api',
]

```

<a name="2-generating-api"></a>

## 2. Generating API

<a name="21-create-model"></a>

### 2.1. Create a model

- Django uses an ORM, so it maps Python code to SQL commands, so CRUD operations are abstracted by its ORM

```python
# api/models

from django.db import models

class Item(models.Model): # table in a SQL database
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
```

- Run migrations

```bash
python manage.py makemigrations # creates migration file
python manage.py migrate # applies migration
```

<a name="22-create-serializer"></a>

### 2.2. Create a serializer

- A class that takes the models and converts back and forth from model to JSON data

```py
# api/serializers.py

from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"
```

<a name="23-create-a-view"></a>

### 2.3. Create a view

- View uses:
  - Model
  - Serializer

```py
# api/views.py

from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
```

<a name="24-config-urls"></a>

### 2.4. Config URLs

- Setup the urls on the app

```py
# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet

router = DefaultRouter()
router.register(r"items", ItemViewSet)

urlpatterns = [
    path("", include(router.urls))
]
```

- Setup the urls on the main Django app

```py
#core/urls.py

from django.contrib import admin
from django.urls import path, include

urlspatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls"))
]
```

<a name="25-registering-models-in-the-admin-panel"></a>

### 2.6. Registering models in the admin panel

```py
# api/admin.py
from django.contrib import admin
from .models import Item

admin.site.register(Item)
```

<a name="26-running-the-server"></a>

### 2.6 Running the server

```py
python manage.py createsuperuser
python manage.py runserver
```

<a name="3-dockerizing-the-project"></a>

## 3. Dockerizing the project

<a name="31-create-a-dockerfile"></a>

### 3.1. Create a Dockerfile

```Dockerfile
FROM python:3.11

# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt  # Fixed typo here

COPY . /app/

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
```

<a name="32-create-a-docker-compose-file"></a>

### 3.2. Create a docker-compose file

```yml
services:
  web:
    build: .
    container_name: django_app
    ports:
      # -"host_port:container_port"
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DEBUG=True
```

<a name="33-build-and-run-the-container"></a>

### 3.3. Build and run the container

```bash
docker-compose up --build
``
```

## 4. Types of views

### 4.1. Function-Based Views

- Standard way Django views to handle API requests using function
- Rely on `@api_view` decorator

```py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def item_list(request):
    if request.method == "GET"
        return Response({"message": "List of items"}, status=status.HTTP_200_OK)
    elif request.method == "POST"
        return Response({"message": "Item created"}, status=status.HTTP_201_CREATED)
```

#### When to use it?

- Simple API endpoints
- Minimal boilerplate

### 4.2. Class-Based Views (APIView)

- `APIView` is a base class that provides request methods as class methods instead of functions

```py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ItemList(APIView):
    # class method
    def get(self, request):
        return Response({"message": "List of items"}, status=status.HTTP_200_OK)

    def post(self, request):
        return Response({"message": "Item created"}, status=status.HTTP_201_CREATED)
```

#### When to use it?

- Simple API endpoints, but with classes inheritance
- Makes the code more modular and maintainable than using FBV

### 4.3. Mixins

- Mixins are reusable classes that provide pre-built behaviors for handling CRUD operations
- Instead of writing GET, POST, PUT and DELETE manually, inherit the mixins

```py
from rest_framework import mixins, generics
from .models import Item
from .serializers import ItemSerializer

class ItemList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

#### When to use it?

- When you need partial CRUD functionality
- When using generic views, but with some level of customization

### 4.4 Generic Views (Simplified Mixins)

- DRF provides generic class-based views, which combine mixins automatically to reduce boilerplate code

```py
from rest_framework import generics
from .models import Item
from .serializers import ItemSerializer

class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
```

#### When to use it?

- Working with standard CRUD operations
- Whan you want to avoid repetitive mixins

#### Common Generic Views

- ListAPIView: GET | read-only list of objects
- RetrieveAPIView: GET | get a single object
- CreateAPIView: POST | create a new object
- UpdateAPIView: PUT/PATCH | update a single object
- DeleteAPIView: DELETE | delete a single object
- ListCreateAPIView: GET + POST | Combines ListAPIView + CreateAPIView
- RetrieveUpdateDestroyAPIView: GET (1) + PUT/PATCH + DELETE | Combines Retrieve, Update and Delete

### 4.5. ViewSets
