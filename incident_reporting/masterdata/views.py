from django.shortcuts import render, redirect, get_object_or_404
from masterdata.models import Department, Division
from masterdata.forms import DepartmentForm, DivisionForm
from django.contrib.auth.decorators import login_required
from accounts.decorators import audit_trail_decorator





# 🔸 Manage Departments
@login_required
@audit_trail_decorator
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


# 🔸 Edit Department
@login_required
@audit_trail_decorator
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


# 🔸 Delete Department
@login_required
@audit_trail_decorator
def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk, is_deleted=False)
    department.is_deleted = True
    department.save()
    return redirect('manage_departments')


# 🔹 Manage Divisions
@login_required
@audit_trail_decorator
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


# 🔹 Edit Division
@login_required
@audit_trail_decorator
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


# 🔹 Delete Division
@login_required
@audit_trail_decorator
def delete_division(request, pk):
    division = get_object_or_404(Division, pk=pk, is_deleted=False)
    division.is_deleted = True
    division.save()
    return redirect('manage_divisions')
