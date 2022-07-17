from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import*
urlpatterns = [
    path('', home, name='home'),
    path('notes', notes, name='notes'),
    path('blog', blog, name='blog'),
    path('blogdetails/<int:pk>', blogDetails, name='blog_details'),
    path('signup', signup, name='signup'),
    path('login', login, name='login'),
    path('homework', homework, name='homework'),
    path('homework_delete/<int:pk>', delete_homework, name='homework_delete'),
    path('delete_note/<int:pk>', delete_note, name='delete-note'),
    path('NotesDetails/<int:pk>', NoteDetailsView.as_view(), name='note-detail'),
    path('todo', todo, name='todo'),
    path('todo/<int:pk>', todo_delete, name='todo-delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
