'''Schafer, C. (2019). CoreyMSchafer/code_snippets. [online]
GitHub. Available at: https://github.com/CoreyMSchafer/code_snippets/tree/master/Django_Blog
[Accessed 1 Dec. 2018].'''
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProfileForm
from django.contrib.auth.decorators import login_required
from users.models import Profile
from django.contrib.auth import authenticate, login


def register(request):
    if request.method == 'POST':
        form= UserRegisterForm(request.POST)
        if form.is_valid():
            form.save() #save user and hash password
            username= form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!') #f string as it contains braces
            user = request.POST['username']
            password = request.POST['password1']
            #authenticate user then login
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('blog-home')
    else:
        form= UserRegisterForm()
    return render (request,'users/register.html',{'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
