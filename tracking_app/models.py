from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

# Create your models here.


class Project(models.Model):
    STATUS_CHOICES = [
        ("not_started", "Not Started"),
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
    ]

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_projects"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="not_started"
    )
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_progress(self):
        from django.db.models import Avg

        avg = self.phases.aggregate(avg=Avg("tasks__progress"))["avg"]

        return round(avg) if avg is not None else 0

    def get_status(self):
        progress = self.get_progress()

        if progress == 0:
            return "not_started"
        elif progress == 100:
            return "completed"
        return "ongoing"


class Phase(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="phases"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_progress(self):
        from django.db.models import Avg

        avg = self.tasks.aggregate(avg=Avg("progress"))["avg"]

        return round(avg) if avg is not None else 0


class Task(models.Model):
    STATUS_CHOICES = [
        ("not_started", "Not Started"),
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
    ]

    phase = models.ForeignKey(
        Phase, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="not_started"
    )
    progress = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
