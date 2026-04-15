from django.shortcuts import render, redirect

from .models import *


# Create your views here.
def home(request):
    return render(request, 'tracking_app/main.html')

def project_list(request):
    projects = Project.objects.all()

    context = {'projects':projects}

    return render(request, 'tracking_app/project_list.html', context)