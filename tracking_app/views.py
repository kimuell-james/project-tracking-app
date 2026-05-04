from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse

from .models import *
from .forms import *
from .decorators import unauthenticated_user


@unauthenticated_user
def login_user(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                return redirect("login")
    else:
        form = LoginForm()

    context = {"form": form}

    return render(request, "tracking_app/login_page.html", context)


@login_required(login_url="/login/")
def logout_user(request):
    logout(request)
    return redirect("login")


@login_required(login_url="/login/")
def home(request):
    users = User.objects.all()

    context = {"users": users}

    return render(request, "tracking_app/main.html", context)


@login_required(login_url="/login/")
def project_list(request):
    projects = Project.objects.all()

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Project added successfully!")
            return redirect("project_list")
    else:
        form = ProjectForm()

    context = {"projects": projects, "form": form}

    return render(request, "tracking_app/project_list.html", context)


@login_required(login_url="/login/")
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    phases = Phase.objects.filter(project=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project detail updated successfully!")
            return redirect("project_list")
    else:
        form = ProjectForm(instance=project)

    context = {"project": project, "phases": phases, "form": form}

    return render(request, "tracking_app/project_detail.html", context)


@login_required(login_url="/login/")
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project deleted successfully!")
        return redirect("project_list")

    return redirect("project_list")


@login_required
def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    desired = request.GET.get("value")

    if desired == "true":
        task.status = "completed"
        task.progress = 100
    else:
        task.status = "not_started"
        task.progress = 0

    task.save()

    phase = task.phase
    project = phase.project

    return JsonResponse(
        {
            "status": task.status,
            "progress": task.progress,
            "phase_id": phase.id,
            "phase_progress": phase.get_progress(),
            "project_progress": project.get_progress(),
        }
    )
