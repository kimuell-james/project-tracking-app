from django.shortcuts import render, get_object_or_404, redirect


from .models import *


# Create your views here.
def home(request):
    return render(request, 'tracking_app/main.html')

def project_list(request):
    projects = Project.objects.all()

    context = {'projects':projects}

    return render(request, 'tracking_app/project_list.html', context)

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    phases = Phase.objects.filter(project=project)

    context = {'project':project, 'phases':phases}

    return render(request, 'tracking_app/project_detail.html', context)

