from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib import messages
from workout import models
from workout.forms import WorkoutForm, SetExerciseRelationshipForm


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


def edit_set_exercise_relationship(request, id):
    relationship = models.SetExerciseRelationship.objects.get(id=id,
                                                              user=request.user)  # noqa
    if request.method == 'POST':
        form = SetExerciseRelationshipForm(request.POST,
                                           instance=relationship,
                                           user=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Relationship changed with success!")
            return redirect('user:my-profile')
    form = SetExerciseRelationshipForm(instance=relationship,
                                       user=request.user)
    context = {
        'form': form,
        'is_add_set_exercise_relationship': True,
        "title": "Change Set X Exercise relationship - ",
    }
    return render(request, "user/myworkout/myworkouts.html", context)


def delete_set_exercise_relationship(request, id):
    relationship = models.SetExerciseRelationship.objects.get(pk=id,
                                                              user=request.user)  # noqa
    if relationship.user == request.user:
        relationship.delete()
        messages.success(request, "Relatioship deleted with success!")
    else:
        messages.error(
            request, "Yo don't have permission for this.")
        return redirect('home:homepage')
    return redirect('user:my-profile')


def add_workout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            form.save_m2m()
            return redirect('user:my-profile')
    else:
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
        'workout': workout,
        'is_myworkout': True,
        "title": f"{workout.name} - ",
        "total_exercises": count,
    }
    return render(request, "user/myworkout/myworkouts.html", context)


def edit_myworkout(request, slug):
    workout = models.Workout.objects.get(slug=slug, user=request.user)
    if request.method == 'POST':
        form = WorkoutForm(request.POST,
                           instance=workout)
        if form.is_valid():
            form.save()
            messages.success(request, "Workout changed with success!")
            return redirect('user:my-profile')
    form = WorkoutForm(instance=workout)
    context = {
        'form': form,
        'is_add_workout': True,
        "title": "Change Workout - ",
    }
    return render(request, "user/myworkout/myworkouts.html", context)


def delete_myworkout(request, slug):
    workout = models.Workout.objects.get(slug=slug, user=request.user)
    if workout.user == request.user:
        workout.delete()
        messages.success(request, "Workout deleted with success!")
    else:
        messages.error(
            request, "Yo don't have permission for this.")
        return redirect('home:homepage')
    return redirect('user:my-profile')


def myworkouts(request):
    myworkouts = models.Workout.objects.filter(user=request.user)
    context = {
        'workouts': myworkouts,
        'is_myworkouts': True,
        "title": "My Workouts - ",
    }
    return render(request, "user/myworkout/myworkouts.html", context)
