from django.shortcuts import render,redirect
from . import forms 
from django.contrib import messages
from django.contrib.auth.forms import  AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login , update_session_auth_hash, logout


def home(request):
    return render(request, 'home.html')


def user_register(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Account Created Successfully')
            form.save()
            return redirect('profile')
    else:
        form = forms.RegistrationForm()
    return render(request, 'register.html', {'form' : form})


def user_login(request):
    if request.method=="POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            user_pass = form.cleaned_data['password']
            user = authenticate(username= user_name, password= user_pass)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form':form} )


def user_logout(request):
    logout(request)
    messages.success(request, ' Successfully Logged Out ')
    return redirect('home')

def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = forms.ChangeUserData(request.POST, instance= request.user)
            if form.is_valid():
                messages.success(request, 'Account updated successfully')
                form.save()
        else:
            
            form = forms.ChangeUserData(instance= request.user)
        
        return render(request, 'profile.html', {'form' : form})
    else:
        return redirect('login')
    

def pass_change(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                # password update korbe
                update_session_auth_hash(request, form.user)
                return redirect('profile')
        else:
            form = PasswordChangeForm(user=request.user)
        return render(request, 'passchange.html', {'form': form})
    else:
        return redirect('login')


def pass_change2(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SetPasswordForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                # password update korbe
                update_session_auth_hash(request, form.user)
                return redirect('profile')
        else:
            form = SetPasswordForm(user=request.user)
        return render(request, 'passchange.html', {'form': form})
    else:
        return redirect('login')