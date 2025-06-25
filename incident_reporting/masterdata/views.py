from django.shortcuts import render, redirect, get_object_or_404
from masterdata.models import Department, Division, IncidentSeverity, IncidentStatus
from masterdata.forms import DepartmentForm, DivisionForm, IncidentSeverityForm, IncidentStatusForm
from django.contrib.auth.decorators import login_required
from accounts.decorators import audit_trail_decorator, role_level_required
from django.http import JsonResponse
from .models import RoleStatusMapping
from .forms import RoleStatusMappingForm



#  Manage Departments
@login_required
@audit_trail_decorator
@role_level_required(1)
def manage_departments(request):
    departments = Department.objects.filter(is_deleted=False)  # Filter soft-deleted
    form = DepartmentForm()

    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_departments')

    return render(request, 'department.html', {
        'departments': departments,
        'form': form,
        'edit_mode': False,
    })


#  Edit Department
@login_required
@audit_trail_decorator
@role_level_required(1)
def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    departments = Department.objects.all()
    form = DepartmentForm(instance=department)

    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('manage_departments')

    return render(request, 'department.html', {
        'departments': departments,
        'form': form,
        'edit_mode': True,
        'editing_id': pk,
    })


# Delete Department
@login_required
@audit_trail_decorator
@role_level_required(1)
def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk, is_deleted=False)
    department.is_deleted = True
    department.save()
    return redirect('manage_departments')


# Manage Divisions
@login_required
@audit_trail_decorator
@role_level_required(1)
def manage_divisions(request):
    divisions = Division.objects.filter(is_deleted=False)
    form = DivisionForm()

    if request.method == 'POST':
        form = DivisionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_divisions')

    return render(request, 'divisions.html', {
        'divisions': divisions,
        'form': form,
        'edit_mode': False,
    })


# Edit Division
@login_required
@audit_trail_decorator
@role_level_required(1)
def edit_division(request, pk):
    division = get_object_or_404(Division, pk=pk)
    divisions = Division.objects.all()
    form = DivisionForm(instance=division)

    if request.method == 'POST':
        form = DivisionForm(request.POST, instance=division)
        if form.is_valid():
            form.save()
            return redirect('manage_divisions')

    return render(request, 'divisions.html', {
        'divisions': divisions,
        'form': form,
        'edit_mode': True,
        'editing_id': pk,
    })


#  Delete Division
@login_required
@audit_trail_decorator
@role_level_required(1)
def delete_division(request, pk):
    division = get_object_or_404(Division, pk=pk, is_deleted=False)
    division.is_deleted = True
    division.save()
    return redirect('manage_divisions')


def manage_severity(request):
    severity=IncidentSeverity.objects.filter(is_deleted=False)
    if request.method=='POST':
        form=IncidentSeverityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_severity')
    else:
        form=IncidentSeverityForm()
    return render(request,'severity.html',{'form':form,'severities':severity,'edit_mode':False})


def edit_severity(request,pk):
    severity = get_object_or_404(IncidentSeverity, pk=pk)
    severities = IncidentSeverity.objects.filter(is_deleted=False)
    form = IncidentSeverityForm(instance=severity)

    if request.method == 'POST':
        form = IncidentSeverityForm(request.POST, instance=severity)
        if form.is_valid():
            form.save()
            return redirect('manage_severity')

    return render(request,'severity.html',{'form':form,'severities':severities,'edit_mode':True})

def delete_severity(request,pk):
    severity = get_object_or_404(IncidentSeverity, pk=pk)
    severity.is_deleted = True
    severity.save()
    return redirect('manage_severity')


def manage_status(request):
    statuses = IncidentStatus.objects.filter(is_deleted=False)

    if request.method == 'POST':
        form = IncidentStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_status')
    else:
        form = IncidentStatusForm()

    return render(request, 'status.html', {
        'form': form,
        'statuses': statuses,
        'edit_mode': False,
    })


def edit_status(request, pk):
    status = get_object_or_404(IncidentStatus, pk=pk)
    statuses = IncidentStatus.objects.filter(is_deleted=False)

    if request.method == 'POST':
        form = IncidentStatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            return redirect('manage_status')
    else:
        form = IncidentStatusForm(instance=status)

    return render(request, 'status.html', {
        'form': form,
        'statuses': statuses,
        'edit_mode': True,
        'edit_id': pk,
    })


def manage_severity(request):
    severity=IncidentSeverity.objects.filter(is_deleted=False)
    if request.method=='POST':
        form=IncidentSeverityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_severity')
    else:
        form=IncidentSeverityForm()
    return render(request,'severity.html',{'form':form,'severities':severity,'edit_mode':False})


def edit_severity(request,pk):
    severity = get_object_or_404(IncidentSeverity, pk=pk)
    severities = IncidentSeverity.objects.filter(is_deleted=False)
    form = IncidentSeverityForm(instance=severity)

    if request.method == 'POST':
        form = IncidentSeverityForm(request.POST, instance=severity)
        if form.is_valid():
            form.save()
            return redirect('manage_severity')

    return render(request,'severity.html',{'form':form,'severities':severities,'edit_mode':True})

def delete_severity(request,pk):
    severity = get_object_or_404(IncidentSeverity, pk=pk)
    severity.is_deleted = True
    severity.save()
    return redirect('manage_severity')


def manage_status(request):
    statuses = IncidentStatus.objects.filter(is_deleted=False)

    if request.method == 'POST':
        form = IncidentStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_status')
    else:
        form = IncidentStatusForm()

    return render(request, 'status.html', {
        'form': form,
        'statuses': statuses,
        'edit_mode': False,
    })


def edit_status(request, pk):
    status = get_object_or_404(IncidentStatus, pk=pk)
    statuses = IncidentStatus.objects.filter(is_deleted=False)

    if request.method == 'POST':
        form = IncidentStatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            return redirect('manage_status')
    else:
        form = IncidentStatusForm(instance=status)

    return render(request, 'status.html', {
        'form': form,
        'statuses': statuses,
        'edit_mode': True,
        'edit_id': pk,
    })


def delete_status(request, pk):
    status = get_object_or_404(IncidentStatus, pk=pk)
    status.is_deleted = True
    status.save()
    return redirect('manage_status')




def role_status_mapping_view(request):
    mappings = RoleStatusMapping.objects.all()
    form = RoleStatusMappingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('role-status-mapping')

    return render(request, 'role_status_mapping.html', {
        'form': form,
        'allMappings': mappings,
    })

def edit_role_status_mapping(request, pk):
    mapping = get_object_or_404(RoleStatusMapping, pk=pk)
    form = RoleStatusMappingForm(request.POST or None, instance=mapping)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('role-status-mapping')
    return render(request, 'role_status_mapping.html', {
        'form': form,
        'allMappings': RoleStatusMapping.objects.all(),
        'edit_mode': True,
        'editing_id': pk,
    })


def delete_role_status_mapping(request, pk):
    mapping = get_object_or_404(RoleStatusMapping, pk=pk)
    mapping.delete()
    return redirect('role-status-mapping')
