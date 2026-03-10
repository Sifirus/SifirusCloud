from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *


def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('login')

        else:
            return render(request, 'users/register_form.html', {'form': form})

    else:
        form = RegisterForm()
        return render(request, 'users/register_form.html', {'form': form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == 'POST':
        form = LoginForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('index'))

        else:
            return render(request, 'users/login_form.html', {'form': form})

    else:
        form = LoginForm()
        return render(request, 'users/login_form.html', {'form': form})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect(reverse('index'))
    else:
        return redirect('login')


@login_required(login_url='login')
def render_profile(request, user_id):
    profile = Profile.objects.filter(user_id=user_id).first()
    return render(request, 'users/profile.html', {'profile': profile})


@login_required(login_url='login')
def edit_profile(request, user_id):
    profile = Profile.objects.filter(user_id=user_id).first()
    if request.user != profile.user:
        return redirect('profile', user_id=user_id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=user_id)
        else:
            return render(request, 'users/profile_edit_form.html', {'form': form})
    else:
        form = ProfileForm(instance=profile)
        return render(request, 'users/profile_edit_form.html', {'form': form})
