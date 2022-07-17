from django.contrib import admin
from .models import Homework, Notes, Tutorial, Todo


admin.site.register(Notes)
admin.site.register(Homework)
admin.site.register(Tutorial)
admin.site.register(Todo)


class TutorialAdmin(admin.ModelAdmin):
    pass

# Register your models here.
