from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .models import Homework, Notes
from .forms import NotesForm, HomeworkForm, TodoForm
from django.contrib import messages
from django.views import View
from django.contrib import auth
from django.contrib.auth.models import User
from .models import*


def blog(request):
    tut = Tutorial.objects.all()
    context = {
        'tut': tut
    }
    return render(request, 'blog.html', context)


def blogDetails(request, pk):
    tut = Tutorial.objects.get(id=pk)
    context = {
        'tut': tut
    }
    return render(request, 'blogdetails.html', context)


def signup(request):
    if request.method != "POST":
        return render(request, 'signup.html')
    username = request.POST['username']
    email = request.POST['email']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    if password1 == password2:
        if User.objects.filter(username=username).exists():
            print('username already exist')
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            print("email already exist")
            return redirect('signup')
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password1)
            user.save()
            return redirect(login)
    else:
        print("password did't match")
        return redirect('signup')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            print("invalid credantial")
            return redirect('login')
    return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')


def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(
                user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
        messages.success(
            request, f'Notes added from{request.user.username}successfully')
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {
        'form': form, 'notes': notes
    }
    return render(request, 'notes.html', context)


def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')


class NoteDetailsView(View):
    def get(self, request, *args, **kwargs):
        notes = get_object_or_404(Notes, pk=kwargs['pk'])
        return render(request, 'details.html', {'notes': notes})


def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                finished = finished == 'on'
            except Exception:
                finished = False
            homework = Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                is_finished=finished)
            homework.save()
            print(homework)
            messages.success(
                request, f'homework added from{request.user.username}successfully!!')
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    homework_done = len(homework) == 0
    context = {'homework': homework,
               'homework_done': homework_done, 'form': form}
    return render(request, 'homework.html', context)


def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')


def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                finished = finished == 'on'
            except Exception:
                finished = False
                todo = Todo(
                    user=request.user,
                    title=request.POST['title'],
                    is_finished=finished
                )
                todo.save()
                messages.success(
                    request, f"Todo added {request.user.username}!!!")
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    context = {
        'todo': todo,
        'form': form
    }
    return render(request, 'todo.html', context)


def todo_delete(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')


# Create your views here.
