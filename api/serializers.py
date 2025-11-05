from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Project, Task, Tag, UserProfile


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'created_at', 'updated_at']


class ProjectSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'owner_username', 'created_at', 'updated_at']


class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.ReadOnlyField(source='project.name')
    assignee_username = serializers.ReadOnlyField(source='assignee.username')
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, write_only=True, required=False, source='tags'
    )

    class Meta:
        model = Task
        fields = [
            'id', 'project', 'project_name', 'title', 'description', 'status', 'priority',
            'due_date', 'assignee', 'assignee_username', 'tags', 'tag_ids', 'created_at', 'updated_at'
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'username', 'bio', 'created_at', 'updated_at']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        UserProfile.objects.create(user=user)
        return user


