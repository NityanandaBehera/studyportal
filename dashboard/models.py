from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from embed_video.fields import EmbedVideoField


class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name = "notes"
        verbose_name_plural = "notes"

    def __str__(self):
        return self.title


class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=48)
    description = models.TextField()
    due = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Tutorial(models.Model):
    tutorial_title = models.CharField(max_length=100)
    tutorial_body = models.TextField()
    tutorial_video = EmbedVideoField()

    def __str__(self):
        return self.tutorial_title


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title
# Create your models here.
