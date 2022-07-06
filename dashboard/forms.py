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
        Widgets = {'due': DateInput()}
        fields = ['subject', 'title', 'description', 'due', 'is_finished']
