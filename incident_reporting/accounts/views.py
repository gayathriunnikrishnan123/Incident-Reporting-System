from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms import UserCreationForm, InternalUserEditForm
from accounts.models import CustomUserProfile

# Create your views here.


def loginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        validUser = authenticate(request, username=username, password=password)

        if validUser is not None:
            login(request, validUser)
            return redirect("dashboard")
        else:
            messages.error(request, "invalid username and password")

    return render(request, "login.html")


@login_required
def dashboardView(request):
    return HttpResponse("dashboard")


@login_required
def createUserView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            CustomUserProfile.objects.create_user(
                email=data["email"],
                password=data["password"],
                fullname=data["fullname"],
                phone=data["phone"],
                default_department=data["default_department"],
                default_division=data["default_division"],
            )
            messages.success(request, "User created successfully.")
            return redirect("show-users")
    else:
        form = UserCreationForm()

    return render(request, "create_user.html", {"form": form})


@login_required
def editUserView(request, userId):
    userData = get_object_or_404(CustomUserProfile, id=userId)
    if request.method == "POST":
        form = InternalUserEditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            email_exists = CustomUserProfile.objects.filter(email=data['email']).exclude(id=userId).exists()
            phone_exists = CustomUserProfile.objects.filter(phone=data['phone']).exclude(id=userId).exists()

            if email_exists:
                form.add_error('email', 'Email already exists.')
            if phone_exists:
                form.add_error('phone', 'Phone number already exists.')

            if not form.errors:
                userData.fullname=data['fullname']
                userData.email=data['email']
                userData.phone=data['phone']
                userData.default_department = data['default_department']
                userData.default_division = data['default_division']
                userData.save()
                # messages.success(request, "User updated successfully.")
                print("user data updated")
                return redirect("show-users")
    else:
        form = InternalUserEditForm(initial={
            'fullname': userData.fullname,
            'email': userData.email,
            'phone': userData.phone,
            'default_department': userData.default_department,
            'default_division': userData.default_division,
        })

    return render(request,"edit_user.html", {"form": form})



@login_required
def deleteUserView(request, userId):
    userData = CustomUserProfile.objects.get(id=userId)
    userData.delete()
    return redirect('show-users')



@login_required
def userListView(request):
    allUsers = CustomUserProfile.objects.all()
    return render(request, 'userMaster.html', {'users': allUsers})