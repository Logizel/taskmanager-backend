from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Project, Task, Tag, UserProfile
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = "Seed demo data for projects, tasks, tags, and users"

    def handle(self, *args, **options):
        self.stdout.write("Seeding demo data...")

        # Users
        users = []
        for username in ["demo", "alice", "bob"]:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password("password")
                user.email = f"{username}@example.com"
                user.save()
                UserProfile.objects.create(user=user, bio=f"Bio for {username}")
            users.append(user)

        # Tags
        tag_names = [
            ("backend", "#ef4444"),
            ("frontend", "#22c55e"),
            ("bug", "#f59e0b"),
            ("urgent", "#3b82f6"),
        ]
        tags = []
        for name, color in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name, defaults={"color": color})
            tags.append(tag)

        # Projects and Tasks
        for user in users:
            for i in range(1, 3):
                project, _ = Project.objects.get_or_create(
                    name=f"{user.username.capitalize()} Project {i}",
                    owner=user,
                    defaults={"description": f"Demo project {i} for {user.username}"},
                )
                for j in range(1, 6):
                    task, _ = Task.objects.get_or_create(
                        project=project,
                        title=f"Task {j} for {project.name}",
                        defaults={
                            "description": "This is a demo task.",
                            "status": random.choice(["todo", "in_progress", "done"]),
                            "priority": random.choice(["low", "medium", "high"]),
                            "due_date": date.today() + timedelta(days=random.randint(0, 30)),
                            "assignee": random.choice(users),
                        },
                    )
                    task.tags.set(random.sample(tags, k=random.randint(0, len(tags))))

        self.stdout.write(self.style.SUCCESS("Demo data seeded."))


