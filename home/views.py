from django.contrib import messages
from django.shortcuts import render
from workout.views import JointsViewApi, MusclesViewApi, ExercisesViewApi, BonesViewApi


def home(request):
    messages.info(request, "A great part of images in this site were taken from <a target='blank' href='https://thenounproject.com'><strong>The Noun Project!</strong></a> ")
    return render(request, 'home/home.html')


def api(request):
    exercises = ExercisesViewApi().get_queryset()

    context = {
        'title': 'About API - ',
        'exercises': exercises.order_by('id'),
    }
    return render(request, 'home/api.html', context)
