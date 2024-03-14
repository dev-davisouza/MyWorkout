from django.shortcuts import redirect, render
from django.db.models import Q
from . import models
from .forms import WorkoutForm, SetExerciseRelationshipForm
from django.contrib import messages


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


def search(request):
    # Search system
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

    filter_by = request.GET.get('filter_by')
    if filter_by is not None:
        if filter_by == 'all':  # All structures
            pass
        elif filter_by == 'bone':  # Just bones
            objects = [bones,] 
        elif filter_by == 'joint':  # Just joints
            objects = [joints,] 
        elif filter_by == 'muscle':  # Just muscles
            objects = [muscles,] 
    else:
        objects = [bones, joints, muscles]

    if not search_term or not bones and not muscles and not joints:
        return render(request, 'partials/404.html', status=404)

    filter_str = f'q={search_term}&filter_by={filter_by}'

    return render(request, 'search.html', context={
        'search_term': search_term,
        'objects': objects,
        'is_search': True,
        'filter': filter_str,
        "title": f"'{search_term}' - ",
    })


def add_set_exercise_relationship(request):
    if request.method == 'POST':
        form = SetExerciseRelationshipForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            messages.success(request, "New Relationship added!")
            return redirect('workout:add-set_exercise_relationship')

    form = SetExerciseRelationshipForm()
    context = {
        'form': form,
        'is_add_set_exercise_relationship': True,
        "title": "Add Set X Exercise relationship - ",
    }
    return render(request, "user/myworkout/myworkouts.html", context)


def add_workout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            return redirect('user:my-profile')
    form = WorkoutForm()

    context = {
        'form': form,
        'is_add_workout': True,
        "title": "Make Workout - ",
    }
    return render(request, "user/myworkout/myworkouts.html", context)


def view_myworkout(request, slug):
    workout = models.Workout.objects.get(slug=slug)
    count_exercises = workout.set_exercise_relationships.all()
    count = 0
    for _ in count_exercises:
        count += 1
    context = {
        'item': workout,
        'is_myworkout': True,
        "title": f"{workout.name} - ",
        "total_exercises": count,
    }
    return render(request, "user/myworkout/myworkouts.html", context)
