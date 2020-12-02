from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import MyList
from django.contrib import messages  
from .forms import TodoForm 

# Create your views here.
def index(request):
	items = MyList.objects.all()
	return render(request, 'list/index.html', {'items':items})



def profile(request):
	form = TodoForm()
	if form.is_valid():
		return HttpResponse ('Hello there!')
