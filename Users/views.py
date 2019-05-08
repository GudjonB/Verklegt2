from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from Users.forms.profile_form import ProfileForm
from Users.models import Profiles


def index(request) :
    return render(request, 'Users/index.html' )


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'Users/register.html', {
        'form': UserCreationForm()
    })


def updateProfile(request):
    #profile_obj = Profiles.objects.filter(user=request.user).first()
    profile_obj = Profiles.objects.create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(instance=profile_obj, data=request.POST)
        if form.is_valid():
            profile_obj = form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()
            return redirect('profile')
    return render(request, 'Users/profile.html', {
        'form': ProfileForm(instance=profile_obj)
    })