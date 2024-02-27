from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterUserForm


def register_get(request):
    register_form_data = request.session.get(
        'register_form_data')
    form = RegisterUserForm(register_form_data)
    return render(request, 'user/register.html', {
        'form': form,
        "title": 'Register | '
    })


def register_post(request):
    if not request.POST:
        return redirect("home:homepage")

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterUserForm(POST)

    if form.is_valid():
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request, "Your user was created; now you're logged in!")

        del (request.session['register_form_data'])
        return redirect('home:homepage')

    return redirect("user:register")


def my_profile(request):
    return render(request, "user/user-area.html", context={})