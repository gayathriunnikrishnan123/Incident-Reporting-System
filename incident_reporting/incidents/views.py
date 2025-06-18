from django.shortcuts import render,get_object_or_404, redirect
from incidents.models import Incident
from incidents.forms import IncidentForm
from masterdata.models import IncidentSeverity, IncidentStatus
from accounts.models import CustomUserProfile
from django.core.mail import send_mail 
from django.conf import settings

# Create your views here.




def track_incident_by_token(request):
    token = request.GET.get("token")
    incident = get_object_or_404(Incident, incident_token=token)
    return render(request, "incident_tracking.html", {"incident": incident})




def submit_incident(request):
    if request.method == 'POST':
        form = IncidentForm(request.POST)
        if form.is_valid():
            incident = form.save(commit=False)


            try:
                incident.status = IncidentStatus.objects.get(name="New")
            except IncidentStatus.DoesNotExist:
                incident.status = None


            if incident.department:

                responder = CustomUserProfile.objects.filter(
                    default_department=incident.department, role__name="Responder", is_deleted=False
                ).first()
                incident.assigned_to = responder

            elif incident.division:

                reviewer = CustomUserProfile.objects.filter(
                    default_division=incident.division, role__name="Reviewer", is_deleted=False
                ).first()
                incident.assigned_to = reviewer


            incident.save()


            if incident.email:
                send_mail(
                    subject="Your Incident Token",
                    message=f"Thank you for reporting. Your incident token is: {incident.incident_token}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[incident.email],
                )

            return redirect('incident_success', token=incident.incident_token)

    else:
        form = IncidentForm()

    return render(request, 'submit_incident.html', {'form': form})



def incident_success(request, token):
    return render(request, 'success.html', {'token': token})