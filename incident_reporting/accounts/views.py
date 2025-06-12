from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms import UserCreationForm
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
            CustomUserProfile.objects.create_user(
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
                fullname=form.cleaned_data["fullname"],
                phone=form.cleaned_data["phone"],
                default_department=form.cleaned_data["default_department"],
                default_division=form.cleaned_data["default_division"],
            )
            messages.success(request, "User created successfully.")
            return redirect("show-users")
    else:
        form = UserCreationForm()

    return render(request, "create_user.html", {"form": form})


@login_required
def editUserView(request, userId):
    userData = CustomUserProfile.objects.get(id=userId)
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            dataFromForm = form.changed_data
            userData.email = dataFromForm["email"]
            userData.fullname = dataFromForm["fullname"]
            userData.phone=dataFromForm['phone']
            userData.password=dataFromForm['password']
            userData.default_department=dataFromForm['default_department']
            userData.default_division=dataFromForm['default_division']
            userData.save()
            print("user data updated")
            return redirect("create-user")
    else:
        form=UserCreationForm(initial={
            "email": userData.email,
            "fullname": userData.fullname,
            "phone": userData.phone,
            "password": userData.password,
            "default_department": userData.default_department,
            "default_division": userData.default_division,
        })

    return render(request,"create_user.html", {"form": form})



@login_required
def deleteUserView(request, userId):
    userData = CustomUserProfile.objects.get(id=userId)
    userData.delete()
    return redirect('show-users')



@login_required
def userListView(request):
    allUsers = CustomUserProfile.objects.all()
    return render(request, 'userMaster.html', {'users': allUsers})