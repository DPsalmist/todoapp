from django.shortcuts import render, redirect
from .models import Todo
from django.contrib import messages  
from .forms import TodoForm 
  
############################################### 
  
def index(request): 
  
    item_list = Todo.objects.order_by("-date") 
    if request.method == "POST": 
        form = TodoForm(request.POST) 
        if form.is_valid(): 
            form.save() 
            return redirect('todo') 
    form = TodoForm() 
  
    page = { 
             "forms" : form, 
             "list" : item_list, 
             "title" : "TODO LIST", 
           } 
    return render(request, 'todolist/index.html', page) 

def remove(request, item_id): 
    item = Todo.objects.get(id=item_id) 
    item.delete() 
    messages.info(request, "item removed !!!") 
    return redirect('todo') 
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#from todos.models import Todo


def index(request):
    items = []
    filter = None

    # Get only the user-specific todo items.
    if request.user.is_authenticated:
        filter = request.GET.get('filter')
        print('Filter = ', filter)

        items = filter_results(request.user, filter)

    return render(request, 'index.html', {
        'items': items,
        'filter': filter
    })


def filter_results(user, filter):
    # If filter is completed
    if filter == 'completed':
        return Todo.objects.filter(
            user=user,
            completed=True
        ).order_by('-created_at')

    # Else If filter is pending
    elif filter == 'pending':
        return Todo.objects.filter(
            user=user,
            completed=False
        ).order_by('-created_at')

    # Otherwise
    else:
        return Todo.objects.filter(user=user).order_by('-created_at')


@login_required
def create(request):
    return render(request, 'form.html', {
        'form_type': 'create'
    })


@login_required
def save(request):
    # Get the form data from the request.
    title = request.POST.get('title')
    description = request.POST.get('description')

    # Get hidden form data.
    form_type = request.POST.get('form_type')
    id = request.POST.get('id')

    print('Form type received:', form_type)
    print('Form todo id received:', id)

    # Validation logic
    if title is None or title.strip() == '':
        messages.error(request, 'Item not saved. Please provide the title.')
        return redirect(request.META.get('HTTP_REFERER'))

    if form_type == 'create':
        # Create a new todo item with the data.
        todo = Todo.objects.create(
            title=title,
            description=description,
            created_at=timezone.now(),
            user=request.user
        )
        print('New Todo created: ', todo.__dict__)
    elif form_type == 'edit' and id.isdigit():
        todo = Todo.objects.get(pk=id)
        print('Got todo item: ', todo.__dict__)

        # Save logic
        todo.title = title
        todo.description = description

        todo.save()
        print('Todo updated: ', todo.__dict__)

    # Add save success message
    messages.info(request, 'Todo Item Saved.')
    # Redirect back to index page
    return redirect('index')


@login_required
def edit(request, id):
    print('Received Id: ' + str(id))

    # Fetch todo item by id
    todo = Todo.objects.get(pk=id)
    print('Got todo item: ', todo.__dict__)

    # Check if the logged in user is the creator user of todo.
    if request.user.id != todo.user.id:
        messages.error(
            request, 'You are not authorized to edit this todo item.')
        return redirect('index')

    return render(request, 'form.html', {
        'form_type': 'edit',
        'todo': todo
    })


@login_required
def delete(request, id):
    # Fetch todo item by id
    todo = Todo.objects.get(pk=id)
    print('Got todo item: ', todo.__dict__)

    # Check if the logged in user is the creator user of todo.
    if request.user.id == todo.user.id:
        messages.info(request, 'Todo Item has been deleted.')
        todo.delete()
        return redirect('index')

    messages.error(request, 'You are not authorized to delete this todo item.')
    return redirect('index')


# Create your views here.

# def index(request): #the index view
#     todos = TodoList.objects.all() #quering all todos with the object manager
#     categories = Category.objects.all() #getting all categories with object manager
#     if request.method == "POST": #checking if the request method is a POST
#         if "taskAdd" in request.POST: #checking if there is a request to add a todo
#             title = request.POST["description"] #title
#             date = str(request.POST["date"]) #date
#             category = request.POST["category_select"] #category
#             content = title + " -- " + date + " " + category #content
#             Todo = TodoList(title=title, content=content, due_date=date, 
#             				category=Category.objects.get(name=category))
#             Todo.save() #saving the todo 
#             return redirect("/") #reloading the page
#         if "taskDelete" in request.POST: #checking if there is a request to delete a todo
#             checkedlist = request.POST["checkedbox"] #checked todos to be deleted
#             for todo_id in checkedlist:
#                 todo = TodoList.objects.get(id=int(todo_id)) #getting todo id
#                 todo.delete() #deleting todo
#     return render(request, "index.html", {"todos": todos, "categories":categories})