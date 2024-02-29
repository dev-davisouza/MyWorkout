from django.shortcuts import render
from django.db.models import Q
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

    return render(request, "workout/list-structures.html",
                  {"items": bones, "is_bone": True})


def know_bone(request, slug):
    bone = models.Bone.objects.get(slug=slug)
    context = {
        'is_description': True,
        'item': bone,
        'is_bone': True,
    }
    return render(request, "workout/list-structures.html",
                  context)


def joints(request):
    joints = models.Joint.objects.all()

    return render(request, "workout/list-structures.html",
                  {"items": joints, "is_joint": True})


def know_joint(request, slug):
    joint = models.Joint.objects.get(slug=slug)
    context = {
        "item": joint,
        'is_description': True,
        "is_joint": True,
    }
    return render(request, "workout/list-structures.html",
                  context)


def muscles(request):
    muscles = models.MuscleGroup.objects.all()
    return render(request, "workout/list-structures.html",
                  {"items": muscles, "is_muscle": True})


def know_muscle(request, slug):
    muscle = models.MuscleGroup.objects.get(slug=slug)
    context = {
        'item': muscle,
        'is_description': True,
        "is_muscle": True,
    }
    return render(request, "workout/list-structures.html", context)


def exercises(request):
    exercises = models.Exercise.objects.all()
    context = {'items': exercises,
               'is_exercise': True, }
    return render(request, "workout/list-structures.html", context)


def know_exercise(request, slug):
    exercise = models.Exercise.objects.get(slug=slug)
    context = {
        'item': exercise,
        'is_description': True,
        "is_exercise": True,
    }
    return render(request, "workout/list-structures.html", context)


def search(request):
    search_term = request.GET.get("q")
    if search_term is not None:
        search_term = search_term.strip()
    else:
        search_term = ""

    # Getting the objects:
    muscles = models.MuscleGroup.objects.filter(
        Q(
            Q(name__icontains=search_term) |
            Q(scientific_name__icontains=search_term)
        ),
    )

    joints = models.Joint.objects.filter(
        Q(
            Q(name__icontains=search_term)
        ),
    )

    bones = models.Bone.objects.filter(
        Q(
            Q(name__icontains=search_term)
        ),
    )

    objects = [bones, joints, muscles]

    if not search_term or not bones and not muscles and not joints:
        return render(request, 'partials/404.html', status=404)

    return render(request, 'search.html', context={
        'search_term': search_term,
        'objects': objects,
        'is_search': True,
    })
