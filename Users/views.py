from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from Users.forms.profile_form import ProfileForm
from Users.models import Profiles
from Properties.models import Properties


def index(request) :
    context = {'Properties': Properties.objects.all().order_by('-id')}
    return render(request, 'Users/index.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'Users/register.html', {
        'form': UserCreationForm()
    })

def profile(request):
    profile = Profiles.objects.filter(user=request.user).first()
    if request.method == 'PATCH':
        form = ProfileForm(instance=profile, data=request.PATCH)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user_id = request.id
            profile.save()
            return redirect('profile')
    return render(request, 'Users/profile.html', {
        'form': ProfileForm(instance=profile)
    })