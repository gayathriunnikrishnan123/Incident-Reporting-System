from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms import (
    UserCreationForm,
    InternalUserEditForm,
    RoleCreationForm,
    DepartmentProfileForm,
)
from accounts.models import CustomUserProfile, Role, AuditLog, DepartmentProfile
from accounts.decorators import audit_trail_decorator
from masterdata.models import Department
from django.http import JsonResponse


# Create your views here.


# def loginView(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         validUser = authenticate(request, username=username, password=password)

#         if validUser is not None:
#             login(request, validUser)
#             return redirect("dashboard")
#         else:
#             messages.error(request, "invalid username and password")

#     return render(request, "login.html")


@login_required
@audit_trail_decorator
def dashboardView(request):
    print(request.session)
    return render(request, "dashboard/dashboard.html")


@login_required
@audit_trail_decorator
def systemConfigView(request):
    return render(request, "dashboard/systemConfig.html")


@login_required
@audit_trail_decorator
def userManagementView(request):
    return render(request, "dashboard/userManagement.html")


@login_required
@audit_trail_decorator
def auditLogView(request):
    logs = AuditLog.objects.all()
    return render(request, "dashboard/auditlog.html", {"logs": logs})


@login_required
@audit_trail_decorator
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
@audit_trail_decorator
def editUserView(request, userId):
    userData = get_object_or_404(CustomUserProfile, id=userId)
    if request.method == "POST":
        form = InternalUserEditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            email_exists = (
                CustomUserProfile.objects.filter(email=data["email"])
                .exclude(id=userId)
                .exists()
            )
            phone_exists = (
                CustomUserProfile.objects.filter(phone=data["phone"])
                .exclude(id=userId)
                .exists()
            )

            if email_exists:
                form.add_error("email", "Email already exists.")
            if phone_exists:
                form.add_error("phone", "Phone number already exists.")

            if not form.errors:
                userData.fullname = data["fullname"]
                userData.email = data["email"]
                userData.phone = data["phone"]
                userData.default_department = data["default_department"]
                userData.default_division = data["default_division"]
                userData.save()
                # messages.success(request, "User updated successfully.")
                print("user data updated")
                return redirect("show-users")
    else:
        form = InternalUserEditForm(
            initial={
                "fullname": userData.fullname,
                "email": userData.email,
                "phone": userData.phone,
                "default_department": userData.default_department,
                "default_division": userData.default_division,
            }
        )

    return render(request, "edit_user.html", {"form": form})


@login_required
@audit_trail_decorator
def deleteUserView(request, userId):
    userData = CustomUserProfile.objects.get(id=userId)
    userData.is_deleted = True
    userData.save()
    AuditLog.objects.create(
        user_email=request.user.email,
        function_name="deleteUserView",
        action="Soft Delete",
        path=request.path,
        message=f"Soft deleted user: {userData.email}"
    )
    return redirect("show-users")


@login_required
@audit_trail_decorator
def userListView(request):
    allUsers = CustomUserProfile.objects.filter(is_deleted=False)
    return render(request, "userMaster.html", {"users": allUsers})


@login_required
@audit_trail_decorator
def roleView(request):
    allRoles = Role.objects.filter(is_deleted=False)
    if request.method == "POST":
        form = RoleCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("show-roles")

    else:
        form = RoleCreationForm()
    return render(
        request,
        "roleMaster.html",
        {"form": form, "allRoles": allRoles, "edit_mode": False},
    )


@login_required
@audit_trail_decorator
def editRoleView(request, roleId):
    role = get_object_or_404(Role, id=roleId)
    allRoles = Role.objects.filter(is_deleted=False)
    if request.method == "POST":
        form = RoleCreationForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect("show-roles")

    else:
        form = RoleCreationForm(instance=role)

    return render(
        request,
        "roleMaster.html",
        {"form": form, "allRoles": allRoles, "edit_mode": True},
    )


@login_required
@audit_trail_decorator
def deleteRoleView(request, roleId):
    role = Role.objects.get(id=roleId)
    role.is_deleted=True
    role.save()
    AuditLog.objects.create(
        user_email=request.user.email,
        function_name="deleteRoleView",
        action="Soft Delete",
        path=request.path,
        message=f"Soft deleted role: {role.name}"
    )
    return redirect("show-roles")


@login_required
@audit_trail_decorator
def departmentProfileView(request):
    allMappings = DepartmentProfile.objects.filter(is_deleted=False)
    if request.method == "POST":
        form = DepartmentProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("show-maps")
    else:
        form = DepartmentProfileForm()
    return render(
        request,
        "departmentProfileMaster.html",
        {"form": form, "allMappings": allMappings, "edit_mode": False},
    )


@login_required
@audit_trail_decorator
def departmentProfileEditView(request, mapId):
    map = get_object_or_404(DepartmentProfile, id=mapId)
    allMappings = DepartmentProfile.objects.filter(is_deleted=False)
    if request.method == "POST":
        form = DepartmentProfileForm(request.POST, instance=map)
        if form.is_valid():
            form.save()
            return redirect("show-maps")
    else:
        form = DepartmentProfileForm(instance=map)
    return render(
        request,
        "departmentProfileMaster.html",
        {"form": form, "allMappings": allMappings, "edit_mode": True},
    )


@login_required
@audit_trail_decorator
def departmentProfileDeleteView(request, mapId):
    map = get_object_or_404(DepartmentProfile, id=mapId)
    map.is_deleted=True
    map.save()
    AuditLog.objects.create(
        user_email=request.user.email,
        function_name="departmentProfileDeleteView",
        action="Soft Delete",
        path=request.path,
        message=f"Soft deleted mapping: {map.user}-> {map.role}"
    )
    return redirect("show-maps")



# for auto populating departments from division


def get_departments_by_division(request):
    division_id = request.GET.get("division_id")
    departments = Department.objects.filter(division_id=division_id, is_deleted=False).values("id", "name")
    print(list(departments))
    return JsonResponse(list(departments), safe=False)