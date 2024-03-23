from django.shortcuts import render
from workout.models import Joint


def home(request):
    return render(request, 'home/home.html')


def api(request):
    context = {
        'title': 'About API - '
    }
    return render(request, 'home/api.html', context)


def get_joints(request):
    joints = Joint.objects.all()
    return render(request, 'home/api.html', context={
        'joints': joints,
    })
