from django.shortcuts import render
from . import models


def bones(request):
    is_spine_bone_param = request.GET.get('is_spine_bone')
    if is_spine_bone_param is not None:
        if is_spine_bone_param == '1':  # Just spine bones
            bones = models.Bone.objects.filter(is_spine_bone=True)
        elif is_spine_bone_param == '0':  # All bones
            bones = models.Bone.objects.all()
        elif is_spine_bone_param == '2':  # Except spine bones
            bones = models.Bone.objects.filter(is_spine_bone=False)
    else:
        bones = models.Bone.objects.all()

    context = {
        "items": bones,
        "is_bone": True,
        "title": "Bones - ",
    }

    return render(request, "workout/list-structures.html", context)


def know_bone(request, slug):
    bone = models.Bone.objects.get(slug=slug)
    context = {
        'is_description': True,
        'item': bone,
        'is_bone_detail': True,
        "title": f"{bone.name} - ",
    }
    return render(request, "workout/list-structures.html",
                  context)


def joints(request):
    joints = models.Joint.objects.all()

    context = {
        "items": joints,
        "is_joint": True,
        "title": "Joints - ",
    }

    return render(request, "workout/list-structures.html", context)


def know_joint(request, slug):
    joint = models.Joint.objects.get(slug=slug)
    context = {
        "item": joint,
        'is_description': True,
        "is_joint": True,
        "title": f"{joint.name} - ",

    }
    return render(request, "workout/list-structures.html",
                  context)


def muscles(request):
    muscles = models.MuscleGroup.objects.all()
    context = {
        "items": muscles,
        "is_muscle": True,
        "title": "Muscles - ",
    }

    return render(request, "workout/list-structures.html", context)


def know_muscle(request, slug):
    muscle = models.MuscleGroup.objects.get(slug=slug)
    context = {
        'item': muscle,
        'is_description': True,
        "is_muscle": True,
        "title": f"{muscle.name} - ",
    }
    return render(request, "workout/list-structures.html", context)


def exercises(request):
    exercises = models.Exercise.objects.all()
    context = {'items': exercises,
               'is_exercise': True,
               "title": "Exercises - ", }

    return render(request, "workout/list-structures.html", context)


def know_exercise(request, slug):
    exercise = models.Exercise.objects.get(slug=slug)
    context = {
        'item': exercise,
        'is_description': True,
        "is_exercise": True,
        "title": f"{exercise.name} - ",
    }
    return render(request, "workout/list-structures.html", context)
