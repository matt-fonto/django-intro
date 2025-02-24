from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # forwards requests to the api app

    path('admin/', admin.site.urls), # requests to /admin/ are forwarded to the admin app
    path("api/", include("api.urls")) # requests to /api/ are forwarded to the api app
]
