from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout  # noqa
from .forms import RegisterUserForm, LoginForm
from django.contrib import messages
from .models import User
from workout.models import Workout


def register_get(request):
    register_form_data = request.session.get(
        'register_form_data')
    form = RegisterUserForm(register_form_data)
    return render(request, 'user/register.html', {
        'form': form,
        "title": 'Register | ',
        'is_register': True,
    })


def register_post(request):
    if not request.POST:
        return redirect("home:homepage")

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterUserForm(POST)

    if form.is_valid():
        django_user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name']
        )
        user = form.save(commit=False)
        user.user = django_user
        user.save()

        del (request.session['register_form_data'])
        return redirect('home:homepage')

    return redirect("user:register")


def login_user(request):
    if request.user.is_authenticated:
        return redirect("home:homepage")
    form = LoginForm()
    return render(request, 'user/register.html', {
        'form': form,
        'is_login': True,
    })


def treat_post_login(request):
    if not request.POST:
        return redirect('user:login')

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            login(request, authenticated_user)
            messages.success(request, "You are logged in now. Enjoy it!")
            return redirect('user:my-profile')
        else:
            messages.error(request, 'Invalid credentials')

    return redirect('user:login')


def logout_user(request):
    logout(request)
    return redirect('home:homepage')


def my_profile(request):
    my_workouts = Workout.objects.filter(user=request.user)
    context = {
        'my_workouts': my_workouts,
    }
    return render(request, "user/user-area.html", context)
