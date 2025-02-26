# Django Rest Framework

- DRF is a toolkit for building web APIs

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
   - 4.1. [Function-Based](#41-function-based)
   - 4.2. [Class-Based](#42-class-based)
   - 4.3. [Mixins](#43-mixins)
   - 4.4. [Generic Views](#44-generic-views)
   - 4.5. [ViewSets](#45-viewsets)
5. [DRF Unit Testing](#5-drf-unit-testing)
   - 5.1. [`setUpTestData()`: run tests once before test set](#51-setuptestdata-run-tests-once-before-test-set)
   - 5.2. [Testing authentication](#52-testing-authentication)
6. [Authentication and Permissions](#6-authentication-and-permissions)
   - 6.1. [JWT Authentication](#61-jwt-authentication)
   - 6.2. [Permissions](#62-permissions)
7. [Pagination](#7-pagination)
   - 7.1. [Custom Pagination](#71-custom-pagination)
   - 7.2. [Pagination possibilities (in a nutshell)](#72-pagination-possibilities-in-a-nutshell)
8. [Filtering, Searching, and Ordering](#8-filtering-searching-and-ordering)
9. [Caching](#9-caching)
10. [SerializerMethodField](#10-serializermethodfield)

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

urlpatterns = [
    # forwards requests to the api app

    path('admin/', admin.site.urls), # requests to /admin/ are forwarded to the admin app
    path("api/", include("api.urls")) # requests to /api/ are forwarded to the api app
]
```

<a name="25-registering-models-in-the-admin-panel"></a>

### 2.5. Registering models in the admin panel

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

<a name="4-types-of-views"></a>

## 4. Types of views

<a name="41-function-based"></a>

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

<a name="42-class-based"></a>

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

<a name="43-mixins"></a>

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

<a name="44-generic-views"></a>

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

- When we use generic views in DRF, we typically define the routes using Django's `path` + `include` functions inside `urls.py`.
- Differently from the ViewSets, generic views don't require routers

```py
# app/urls.py

from django.urls import path
from .views import ItemListCreateView, ItemDetailView

urlspatterns = [
    path("items/", ItemListCreateView.as_view(), name="item-list"),
    path("items/<int:pk>", ItemDetailView.as_view(), name="item-detail")
]

# project/urls.py
from django.contrib import admin
from django.urls import path, include

urlspatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")) # include the app url
]
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

- Automatically generates CRUD operations without explicitly defining the methods
- Paired with routes to generate the URLS

```py
# views.py
from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

# urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ItemViewSet

router = DefaultRouter()
router.register(r"items", ItemViewSet)

urlpatterns = [
    path("", include(router.urls))
]
```

<a name="5-drf-unit-testing"></a>

## 5. DRF Unit Testing

- Django uses Python's `unittest` module.
- Create a `tests.py` inside the `api/` app, if not already there

```py
# tests.py

from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Item

class ItemAPITestCase(APITestCase):
    def setUp(self):
        """
        Runs before each test
        """
        # create an user
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # create mock data
        self.item = Item.objects.create(name="Test Item", description="description of item")

        # API urls
        self.list_url = "/api/items/"
        self.detail_url = f"/api/items/{self.item.id}/"

        # Authenticate
        self.client.force_authenticate(user=self.user)

    def test_get_items(self):
        response = self.client.get(self.list_url) # call the api/items
        self.assertEqual(response.status_code, status.HTTP_200_OK) # asserting the status that should return
        self.assertEqual(len(response.data), 1) # asserting the length

    def test_create_item(self):
        item_name = "mock item"
        item_description = "mock description"

        data = {"name": item_name, "description": item_description}
        response = self.client.post(self.list_url, data, format="json") # json post to api/items
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data) # ensure id is in the response
        self.assertEqual(response.data["name"], item_name)
        self.assertEqual(Item.objects.count(), 2) # ensure the item was created. 2, the one created in setUp and the one created in this test

    def test_get_single_item(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item.name)

    def test_update_item(self):
        updated_name = "Updated item"
        updated_description = "Updated description"

        updated_data = {"name": updated_name, "description": updated_description}
        response = self.client.put(self.detail_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, updated_name)

    def test_delete_item(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)

```

- Run tests with

```py
#python manage.py test <app-name>

python manage.py test api
python manage.py test api -v 2 # detailed

docker compose run web python manage.py test api # running tests inside docker
```

<a name="51-setuptestdata-run-tests-once-before-test-set"></a>

### 5.1 `setUpTestData()`: run tests once before test set

- While `setUp()` runs before each test (similar to beforeEach), `setUpTestData()` runs once before the test set (similar to beforeAll or before)

```py
@classmethod
def setUpTestData(cls):
    cls.item = Item.objects.create(name="Persistent item", description="this data is reused")
```

<a name="52-testing-authentication"></a>

### 5.2 Testing authentication

```py
def test_unauthorized_access(self):
    self.client.logout()
    response = self.client.get(self.list_url)
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
```

## 6. Authentication and Permissions

- DRF provides different authentication mechanisms:
  - 1. SessionAuthentication (default, uses django sessions)
  - 2. BasicAuthentication (uses username/password)
  - 3. TokenAuthentication (used for API-based authentication)
  - 4. JWT Authentication (more secure, used in modern APIs)

### 6.1 JWT Authentication

- Install deps

```bash
pip install djangorestframework-simplejwt
```

- Setup the jwt in the settings

```py
#settings.py

INSTALLED_APPS = [
    ...,
    'rest_framework',
    'rest_framework.authtoken',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}
```

- Create tokens for users

```bash
python manage.py drf_create_token <username>
```

- Now, users can authenticate using:

```http
Authorization: Token <your_token>
```

### 6.2 Permissions

- DRF allows restricting access using permission classes

```py
## Custom permission

from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

# Apply to view

from rest_framework.permissions import IsAuthenticated

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated, IsOwner] # ensures users who are authenticated an owners can modify this item
```

- What other relevant permissions are there?

<a name="7-pagination"></a>

## 7. Pagination

```py
# settings.py

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

- Now, API responses include pagination metadata

```json
{
    "count": 100,
    "next": "http://127.0.0.1:8000/api/items/?page=2",
    "previous": null,
    "results": [...]
}
```

<a name="71-custom-pagination"></a>

### 7.1 Custom Pagination

```py
# pagination.py

from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5 # default page size
    page_size_query_param = "page_size" # allows client to control size
    max_page_size = 50 # limit max page size

# apply to view
from rest_framework.generics import ListAPIView
from .models import Item
from .serializers import ItemSerializer
from .pagination import CustomPageNumberPagination

class ItemListView(ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = CustomPageNumberPagination
```

- Now, clients can control page size dynamically

```bash
GET /api/items/?page=1&page_size=10
```

<a name="72-pagination-possibilities-in-a-nutshell"></a>

### 7.2 Pagination possibilities (in a nutshell)

- Global pagination
- Page number (custom pagination)
- Cursor Pagination (infinite scrolling)
- Limit-offset pagination (large data sets)

<a name="8-filtering-searching-and-ordering"></a>

## 8. Filtering, Searching, and Ordering

- Install `django-filter`:

```bash
pip install django-filter
```

- Modify `settings.py`

```py
### settings
INSTALLED_APPS += ['django-filters']

REST_FRAMEWORK['DEFAULT_FILTER_BACKENDS'] = ['django_filters.rest_framework.DjangoFilterBackend']
```

```py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'description'] # FILTERING
    search_fields = ['name', 'description'] # SEARCHING
    ordering_fields = ['name', 'id'] # ORDERING
```

```bash
/api/items/?name=chair # filtering
/api/items/?search=table # searching
/api/items/?ordering=name # ordering
```

<a name="9-caching"></a>

## 9. Caching

- Speeds up API responses

```python
# settings.py

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

- Apply caching to a view

```py
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_creator

class ItemListView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @method_decorator(cache_page(60*15)) # cache for 15 minutes
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
```

<a name="10-serializermethodfield"></a>

## 10. SerializerMethodField

- It's a _read-only field_ that allows customization of how data is presented in API responses
- It allows the inclusion of _computed or related data_ that is not directly a model field
- Computed field that does not exist in the model, but allows dynamic data processing
- It needs a method inside the serializer to determine how this field is populated
  > method should be called get\_<field_name>, where <field_name> matches the serializer field

```py
from rest_framework import serializers

class ExampleSerializer(serializers.ModelSerializer):
    custom_field = serializers.SerializerMethodField()

    def get_custom_field(self, obj):
        return f"Custom data for {obj.name}"
```

### Examples

#### 10.1. Formatting fields (Modify output data)

```py
class ItemSerializer(serializers.ModelSerializer):
    capitalized_name = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields ['id', 'name', 'capitalized_name']

    def get_capitalized_name(self, obj):
        return obj.name.upper()
```

#### 10.2. Fetching related object data (without ForeignKey)

```py
class BookSerializer(serializers.ModelSerializer):
    authon_name = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField() # 10.3. Counting related items (aggregations)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author_name', 'review_count']

    def get_author_name(self, obj):
        return obj.author.full_name

    def get_review_count(self, obj):
        return obj.reviews.count()
```

#### 10.3 Possibilities (in a nutshell)

- Format fields
- Show related data
- Count related items
- Fetch external API data
- Control user permissions

#### 10.4 Benefits

- No need to modify models
- Great for customizing API responses
- Works even with external APIs

<!--
To study:
    - authentication & permissions
    - pagination
    - filtering, searching, ordering
    - authentication
    - caching
    - SerializerMethodField()
 -->
