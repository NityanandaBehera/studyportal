from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .models import Homework, Notes
from .forms import NotesForm, HomeworkForm
from django.contrib import messages
from django.views import View


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
            request, f'Notes added from{request.user.username}sucessfully')
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
                if finished == 'on':
                    finished = True
                else:
                    False
            except Exception:
                finished = False
            homework = Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished)
            homework.save()
            messages.success(
                request, f'homework added from{request.user.username}sucessfully!!')
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    homework_done = len(homework) == 0
    context = {'homework': homework,
               'homework_done': homework_done, 'form': form}
    return render(request, 'homework.html', context)
# Create your views here.
