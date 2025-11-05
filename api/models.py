from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Project(TimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='owned_projects', on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.name


class Tag(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default="#999999")

    def __str__(self) -> str:
        return self.name


class Task(TimeStampedModel):
    STATUS_CHOICES = (
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    )
    PRIORITY_CHOICES = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    )

    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="medium")
    due_date = models.DateField(null=True, blank=True)
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='tasks', null=True, blank=True, on_delete=models.SET_NULL
    )
    tags = models.ManyToManyField(Tag, related_name='tasks', blank=True)

    def __str__(self) -> str:
        return self.title


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"Profile({self.user.username})"

from django.db import models

# Create your models here.
