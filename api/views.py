from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, mixins, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project, Task, Tag, UserProfile
from .serializers import (
    ProjectSerializer,
    TaskSerializer,
    TagSerializer,
    UserProfileSerializer,
    RegisterSerializer,
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        owner = getattr(obj, 'owner', None)
        return owner == request.user


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filterset_fields = ['name']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at', 'name']

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['project', 'status', 'priority', 'assignee', 'tags']
    search_fields = ['title', 'description', 'project__name', 'assignee__username']
    ordering_fields = ['created_at', 'updated_at', 'due_date', 'priority']

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user).select_related('project', 'assignee').prefetch_related('tags')


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

from django.shortcuts import render

# Create your views here.
