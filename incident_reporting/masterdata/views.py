from django.shortcuts import render, redirect
from .models import Department, Division
from .forms import DepartmentForm, DivisionForm
from django.contrib.auth.decorators import user_passes_test

# def is_admin(user):
#     return user.is_superuser or user.groups.filter(name='Admin').exists()

#@user_passes_test(is_admin)
def manage_departments(request):
    departments = Department.objects.all()
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


def edit_department(request, pk):
    department = Department.objects.get(pk=pk)
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


def delete_department(request, pk):
    department = Department.objects.get(pk=pk)
    department.delete()
    return redirect('manage_departments')

#@user_passes_test(is_admin)
def manage_divisions(request):
    divisions = Division.objects.select_related('department').all()
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


def edit_division(request, pk):
    division = Division.objects.get(pk=pk)
    divisions = Division.objects.select_related('department').all()
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


def delete_division(request, pk):
    division = Division.objects.get(pk=pk)
    division.delete()
    return redirect('manage_divisions')