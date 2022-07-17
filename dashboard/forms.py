from datetime import date
from tkinter import Widget
from django import forms
from .models import*


class NotesForm(forms.ModelForm):

    class Meta:
        model = Notes
        fields = ['title', 'description']


class DateInput(forms.DateInput):
    input_type: 'date'


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {
            'date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
        }
        fields = ['subject', 'title', 'description', 'due', 'is_finished']


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'is_finished']
