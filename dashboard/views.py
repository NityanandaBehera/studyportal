from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .models import Homework, Notes
from .forms import NotesForm, HomeworkForm, TodoForm, Dashboard
from django.contrib import messages
from django.views import View
from django.contrib import auth
from django.contrib.auth.models import User
from .models import*
import requests
import wikipedia


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


def book(request):
    if request.method == "POST":
        return _extracted_from_book_3(request)
    else:
        form = Dashboard()
    context = {
        'form': form
    }
    return render(request, 'books.html', context)


# TODO Rename this here and in `book`
def _extracted_from_book_3(request):
    form = Dashboard(request.POST)
    text = request.GET.get('text')
    url = f"https://www.googleapis.com/books/v1/volumes?q={text}"
    r = requests.get(url)
    answer = r.json()
    result_list = []
    for i in range(10):
        result_dict = {
            'title': answer['items'][i]['volumeInfo']['title'],
            'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
            'description': answer['items'][i]['volumeInfo'].get('description'),
            'count': answer['items'][i]['volumeInfo'].get('pageCount'),
            'categories': answer['items'][i]['volumeInfo'].get('categories'),
            'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
            'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks'),
            'preview': answer['items'][i]['volumeInfo'].get('previewLink'),
        }
        result_list.append(result_dict)
        context = {
            'form': form,
            'results': result_list
        }
    return render(request, 'books.html', context)


def dictionary(request):
    if request.method == "POST":
        return _extracted_from_dictionary_3(request)
    form = Dashboard()
    context = {
        'form': form
    }
    print
    return render(request, 'dictionary.html', context)


# TODO Rename this here and in `dictionary`
def _extracted_from_dictionary_3(request):
    form = Dashboard(request.POST)
    text = request.GET.get('text')
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{text}"
    r = requests.get(url)
    answer = r.json()
    try:
        context = _extracted_from_dictionary_9(answer, form, text)
    except Exception:
        context = {
            'form': form,
            'input': text
        }
    return render(request, 'dictionary.html', context)


# TODO Rename this here and in `dictionary`
def _extracted_from_dictionary_9(answer, form, text):
    phonetics = answer[0]['phonetics'][0]['text']
    audio = answer[0]['phonetics'][0]['audio']
    definition = answer[0]['meanings'][0]['definition'][0]['definition']
    example = answer[0]['meanings'][0]['definition'][0]['example']
    synonyms = answer[0]['meanings'][0]['definition'][0]['synonyms']
    return {'form': form, 'input': text, 'phonetics': phonetics, 'audio': audio, 'definition': definition, 'example': example, 'synonyms': synonyms}
# Create your views here.


def wiki(request):
    if request.method == "POST":
        form = Dashboard(request.POST)
        text = request.POST.get('text')
        search = wikipedia.page('cricket')
        context = {
            'form': form,
            'title': search.title,
            'link': search.url,
            'details': search.summary
        }
        return render(request, 'wiki.html', context)
    else:
        form = Dashboard()
        context = {
            'form': form
        }
    return render(request, 'wiki.html', context)
