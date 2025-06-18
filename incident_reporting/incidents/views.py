from django.shortcuts import render, redirect
from .forms import IncidentReportForm

def report_incident(request):
    if request.method == 'POST':
        form = IncidentReportForm(request.POST, request.FILES)
        if form.is_valid():
            return redirect('incident_success')
    else:
        form = IncidentReportForm()

    return render(request, 'report_incident.html', {'form': form})
