import json
from django.http import HttpRequest
from django.shortcuts import render
from workout.views import JointsViewApi, MusclesViewApi, ExercisesViewApi, BonesViewApi


def home(request):
    return render(request, 'home/home.html')


def api(request):
    exercises = ExercisesViewApi().get_queryset()

    context = {
        'title': 'About API - ',
        'exercises': exercises.order_by('id'),
    }
    return render(request, 'home/api.html', context)
