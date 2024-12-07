from django.shortcuts import render, HttpResponse
from .models import TodoItem

# Create your views here.
def home(request): 
    return render(request, 'home.html')

def todos(request):
    # we need to query the todos from the db
    items = TodoItem.objects.all() # fetch the data

    return render(request, "todos.html", {"todos":items}) # pass the data to the template