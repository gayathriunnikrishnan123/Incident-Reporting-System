from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms import (
    UserCreationForm,
    InternalUserEditForm,
    RoleCreationForm,
    DepartmentProfileForm,
    StatusProfileForm,
)
from accounts.models import CustomUserProfile, Role, AuditLog, DepartmentProfile, Menu, RoleStatusMapping
from accounts.decorators import audit_trail_decorator, role_level_required
from masterdata.models import Department, Division
from django.http import JsonResponse
from incidents.models import Incident, IncidentStatus
from incidents.forms import IncidentStatusUpdateForm


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
                request.session['role_id']=depart.role.pk

    role = request.session.get('role_name', None)
    request.session['menus']=ROLE_MENUS.get(role,[])
    print(request.session['role_level'])

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
    role = request.session.get('role_name')
    form = get_status_updateForm_by_role(incident_details, role)
    for i in attachments:
        print(i)
    return render(request,"user_incident_details.html",{'incident_details':incident_details,'attachments':attachments,'status_form': form,'user_role': role,})




#  for reviewer panel


@login_required
@audit_trail_decorator
@role_level_required(2)
def get_my_departments(request):
    my_division=DepartmentProfile.objects.filter(user=request.user,role__name="Reviewer",  department__isnull=True,is_deleted=False).values_list('division_id', flat=True)
    print(list(my_division))  
    my_departments=Department.objects.filter(division_id__in=my_division,is_deleted=False)
    print(my_departments)
    return render(request,"all_departments_reviewer.html",{'my_departments':my_departments})


@login_required
@audit_trail_decorator
@role_level_required(2)
def get_incidents_under_my_departments(request,dept_id):
    department = get_object_or_404(Department, id=dept_id)
    allIncidents=Incident.objects.filter(department_id=dept_id)
    return render(request,"all_incidents_under_department.html",{'allIncidents':allIncidents,'department':department})


# for admin panel

@login_required
@audit_trail_decorator
@role_level_required(1) 
def all_divisions_view(request):
    divisions = Division.objects.all()
    return render(request,"all_divisions_admin.html", {'allDivisions': divisions})


@login_required
@audit_trail_decorator
@role_level_required(1) 
def division_departments_view(request, division_id):
    division = get_object_or_404(Division, pk=division_id, is_deleted=False)
    departments = Department.objects.filter(division=division, is_deleted=False)
    return render(request, 'all_departments_admin.html', {'division': division, 'departments': departments})



#  to do status update based on our team discussuion
# we can setup the allowed status rules
# if its working fine we can move on to db after discussion

ROLE_STATUS_MAP = {
    "Responder": ["In Progress", "Under Transfer", "Completed"],
    "Reviewer": ["Assigned", "Re Assigned", "Under Transfer", "Closed"],
    "Admin": ["New", "Assigned", "Re Assigned", "In Progress", "Under Transfer", "Completed", "Closed", "Rejected"],
}


def get_status_updateForm_by_role(incident,role_name,data=None):
    form=IncidentStatusUpdateForm(data,instance=incident)
    role = Role.objects.filter(name=role_name, is_deleted=False).first()
    if role:
        allowed_status_ids = RoleStatusMapping.objects.filter(role=role,is_deleted=False).values_list('status_id', flat=True)
        form.fields['status'].queryset = IncidentStatus.objects.filter(id__in=allowed_status_ids,is_deleted=False)
    else:
        form.fields['status'].queryset = IncidentStatus.objects.none()

    return form


@login_required
@role_level_required(3)
@audit_trail_decorator
def ajax_update_incident_status(request):
    token=request.POST.get("incident_token")
    role=request.session.get("role_name")

    if not token:
        return JsonResponse({"success": False, "error": "Missing token"}, status=404)
    
    incident = Incident.objects.filter(incident_token=token, is_deleted=False).first()

    if not incident:
        return JsonResponse({"success": False, "error": "Invalid incident token"}, status=404)
    form = get_status_updateForm_by_role(incident, role, request.POST)

    if form.is_valid():
        form.save()
        return JsonResponse({"success": True, "message": "Status updated successfully"})
    else:
        return JsonResponse({"success": False, "errors": form.errors}, status=400)


@login_required
@role_level_required(1)
@audit_trail_decorator
def StatusProfileView(request):
    if request.method=='POST':
        form=StatusProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("show-status-maps")
    else:
        form=StatusProfileForm()
    allMappings=RoleStatusMapping.objects.filter(is_deleted=False)
    return render(
        request,
        "statusMapping.html",
        {"form": form, "allMappings": allMappings, "edit_mode": False},
    )


@login_required
@role_level_required(1)
@audit_trail_decorator
def StatusProfileEditView(request,mapId):
    map=get_object_or_404(RoleStatusMapping,id=mapId)
    if request.method=='POST':
        form=StatusProfileForm(request.POST,instance=map)
        if form.is_valid():
            form.save()
            return redirect("show-status-maps")
    else:
        form=StatusProfileForm(instance=map)
    allMappings=RoleStatusMapping.objects.filter(is_deleted=False)
    return render(
        request,
        "statusMapping.html",
        {"form": form, "allMappings": allMappings, "edit_mode": True},
    )


@login_required
@role_level_required(1)
@audit_trail_decorator
def StatusProfileDeleteView(request,mapId):
    map=get_object_or_404(RoleStatusMapping,id=mapId)
    map.is_deleted=True
    map.save()
    AuditLog.objects.create(
        user_email=request.user.email,
        function_name="StatusProfileDeleteView",
        action="Soft Delete",
        path=request.path,
        message=f"Soft deleted mapping: {map.role}-> {map.status}"
    )
    return redirect("show-status-maps")
