from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import *
from .forms import *


# Create your views here.
def home(request):
    user = User.object.all()

    context = {'user':user}

    return render(request, 'tracking_app/main.html', context)

def project_list(request):
    projects = Project.objects.all()

    context = {'projects':projects}

    return render(request, 'tracking_app/project_list.html', context)

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    phases = Phase.objects.filter(project=project)

    context = {'project':project, 'phases':phases}

    return render(request, 'tracking_app/project_detail.html', context)

def add_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User added successfully!")
            return redirect("project_list")

    else:
        form = ProjectForm()

    return render(request, 'tracking_app/project_form.html', {"form": form})