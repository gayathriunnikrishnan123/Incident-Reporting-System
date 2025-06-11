from django.shortcuts import render, redirect
from .models import Department, Division
from .forms import DepartmentForm, DivisionForm
from django.contrib.auth.decorators import user_passes_test

# def is_admin(user):
#     return user.is_superuser or user.groups.filter(name='Admin').exists()

#@user_passes_test(is_admin)
def manage_departments(request):
    departments = Department.objects.all()
    form = DepartmentForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('manage_departments')

    return render(request, 'department.html', {
        'departments': departments,
        'form': form
    })

#@user_passes_test(is_admin)
def manage_divisions(request):
    divisions = Division.objects.select_related('department').all()
    form = DivisionForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('manage_divisions')

    return render(request, 'divisions.html', {
        'divisions': divisions,
        'form': form
    })