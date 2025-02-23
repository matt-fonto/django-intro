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

```python
# api/models

from django.db import models

class Item(models.Model):
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

## 3. Dockerizing the project

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

### 3.3. Build and run the container

```bash
docker-compose up --build
``
```
