from django.urls import path
from .views import*
urlpatterns = [
    path('', home, name='home'),
    path('notes', notes, name='notes'),
    path('homework', homework, name='homework'),
    path('delete_note/<int:pk>', delete_note, name='delete-note'),
    path('NotesDetails/<int:pk>', NoteDetailsView.as_view(), name='note-detail'),
]
