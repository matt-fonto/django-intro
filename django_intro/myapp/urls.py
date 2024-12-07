from django.urls import path 
from . import views

urlpatterns = [
    #path(route, view, name)
    path("",views.home, name="home")
]