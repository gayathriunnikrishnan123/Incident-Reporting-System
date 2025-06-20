from django.shortcuts import render,get_object_or_404, redirect
from incidents.models import Incident, IncidentAttachment
from incidents.forms import IncidentForm
from masterdata.models import IncidentSeverity, IncidentStatus
from accounts.models import CustomUserProfile, DepartmentProfile
from django.core.mail import send_mail 
from django.conf import settings

# Create your views here.




def track_incident_by_token(request):
    if request.method == 'POST':
        token = request.POST.get("token")

        if not token:
            return render(request, "incident_tracking.html", {"error": "Please enter a valid token."})
        
        incident = Incident.objects.filter(incident_token=token, is_deleted=False).first()

        if not incident:
            return render(request, "incident_tracking.html", {"error": "No incident found for the provided token."})
        return redirect('detailsby_token',token=token)
    
    return render(request, "incident_tracking.html")



def incident_details_by_token(request,token):
    incident_details=get_object_or_404(Incident, incident_token=token, is_deleted=False)
    attachments=incident_details.attachments.all()
    for i in attachments:
        print(i)
    return render(request,"incident_details.html",{'incident_details':incident_details,'attachments':attachments})



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
                responder_profile = DepartmentProfile.objects.filter(department=incident.department,role__name="Responder",is_active=True,is_deleted=False).first()
                if responder_profile:
                    incident.assigned_to = responder_profile.user

            elif incident.division:

                reviewer_profile = DepartmentProfile.objects.filter(division=incident.division,role__name="Reviewer",is_active=True,is_deleted=False).first()
                if reviewer_profile:
                    incident.assigned_to = reviewer_profile.user

            if not incident.assigned_to:
                admin_profile = DepartmentProfile.objects.filter(role__name="Admin",is_active=True,is_deleted=False,division__isnull=True,department__isnull=True).first()   
                if admin_profile:
                    incident.assigned_to = admin_profile.user


            incident.save()

            files = request.FILES.getlist('file')
            for f in files:
                IncidentAttachment.objects.create(incident=incident, file=f)


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
    incident = get_object_or_404(Incident, incident_token=token, is_deleted=False)
    return render(request, 'incident_confirm.html', {'token': incident.incident_token,'email': incident.email,})
