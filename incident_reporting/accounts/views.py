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
from accounts.models import CustomUserProfile, Role, AuditLog, DepartmentProfile, Menu
from accounts.decorators import audit_trail_decorator, role_level_required
from masterdata.models import Department
from django.http import JsonResponse
from incidents.models import Incident


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

ROLE_MENUS = {
    'Admin': [
        {'name': 'Dashboard', 'url': 'dashboard', 'icon': '📊'},
        {'name': 'Master Data', 'url': 'system-config', 'icon': '🛍️'},
        {'name': 'User Management', 'url': 'user-management', 'icon': '👥'},
        {'name': 'All Incidents', 'url': 'all-incidents', 'icon': '📦'},
        {'name': 'Tracking', 'url': 'auditlog', 'icon': '📍'},
    ],
    'Reviewer': [
        {'name': 'Dashboard', 'url': 'dashboard', 'icon': '📊'},
        {'name': 'All Incidents', 'url': 'all-incidents', 'icon': '📦'},
        {'name': 'Tracking', 'url': 'auditlog', 'icon': '📍'},
    ],
    'Responder': [
        {'name': 'Dashboard', 'url': 'dashboard', 'icon': '📊'},
        {'name': 'All Incidents', 'url': 'all-incidents', 'icon': '📦'},
    ],
}



@login_required
@audit_trail_decorator
@role_level_required(3)
def dashboardView(request):
    loggedInUser=request.user
    print(request.session)
    if 'role_name' not in request.session:
        if loggedInUser.is_superuser:
            request.session['role_name'] = 'Admin'
            request.session['role_level'] = 1
        else:
            depart = DepartmentProfile.objects.filter(user=loggedInUser,is_active=True,is_deleted=False,role__is_deleted=False).order_by('role__level').first()
            if depart:
                request.session['role_name'] = depart.role.name
                request.session['role_level'] = depart.role.level

    role = request.session.get('role_name', None)
    request.session['menus']=ROLE_MENUS.get(role,[])


    return render(request, "dashboard/dashboard.html")


@login_required
@audit_trail_decorator
@role_level_required(1)
def systemConfigView(request):
    return render(request, "dashboard/systemConfig.html")


@login_required
@audit_trail_decorator
@role_level_required(1)
def userManagementView(request):
    return render(request, "dashboard/userManagement.html")


@login_required
@audit_trail_decorator
@role_level_required(1)
def auditLogView(request):
    logs = AuditLog.objects.all()
    return render(request, "dashboard/auditlog.html", {"logs": logs})


@login_required
@audit_trail_decorator
@role_level_required(3)
def allIncidentsView(request):
    return render(request, 'dashboard/all_incidents.html')


@login_required
@audit_trail_decorator
@role_level_required(1)
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
@role_level_required(1)
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
@role_level_required(1)
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
@role_level_required(1)
def userListView(request):
    allUsers = CustomUserProfile.objects.filter(is_deleted=False)
    return render(request, "userMaster.html", {"users": allUsers})


@login_required
@audit_trail_decorator
@role_level_required(1)
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
@role_level_required(1)
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
@role_level_required(1)
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
@role_level_required(1)
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
@role_level_required(1)
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
@role_level_required(1)
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

@audit_trail_decorator
def get_departments_by_division(request):
    division_id = request.GET.get("division_id")
    departments = Department.objects.filter(division_id=division_id, is_deleted=False).values("id", "name")
    print(list(departments))
    return JsonResponse(list(departments), safe=False)





@login_required
@audit_trail_decorator
@role_level_required(1)
def get_all_incidents(request):
    role = request.session.get('role_name', None)
    allIncidents=Incident.objects.all()  
    return render(request,"all_user_incidents.html",{'allIncidents':allIncidents})

@login_required
@audit_trail_decorator
@role_level_required(3)
def get_my_incidents(request):
    role = request.session.get('role_name', None)
    allIncidents=Incident.objects.filter(assigned_to=request.user)  
    return render(request,"my_incidents.html",{'allIncidents':allIncidents})



@login_required
@audit_trail_decorator
@role_level_required(3)
def incident_details_by_token(request,token):
    incident_details=get_object_or_404(Incident, incident_token=token, is_deleted=False)
    attachments=incident_details.attachments.all()
    for i in attachments:
        print(i)
    return render(request,"user_incident_details.html",{'incident_details':incident_details,'attachments':attachments})