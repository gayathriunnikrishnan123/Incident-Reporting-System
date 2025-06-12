from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import EmailLoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash,logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request,'home.html')
    
def dashboard(request):
    return render(request,'dashboard.html')

def email_login_view(request):
    if request.method == "POST":
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user is not None:
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('dashboard')
            messages.error(request, "Invalid email or password")
    else:
        form = EmailLoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            logout(request)
            return redirect('login')  
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})