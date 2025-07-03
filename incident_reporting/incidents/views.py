from django.shortcuts import render,get_object_or_404, redirect
from incidents.models import Incident, IncidentAttachment,IncidentQuestion, IncidentAnswer
from incidents.forms import IncidentForm,IncidentQuestionForm
from masterdata.models import IncidentSeverity, IncidentStatus
from accounts.models import CustomUserProfile, DepartmentProfile
from django.core.mail import send_mail 
from django.conf import settings
from django.template.loader import render_to_string
from django.http import JsonResponse

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
    incident_answers=IncidentAnswer.objects.filter(incident=incident_details)
    for i in attachments:
        print(i)
    return render(request,"incident_details.html",{'incident_details':incident_details,'attachments':attachments,'incident_answers':incident_answers})



def submit_incident(request):
    if request.method == 'POST':
        form = IncidentForm(request.POST)
        if form.is_valid():
            incident = form.save(commit=False)


            try:
                incident.status = IncidentStatus.objects.get(name="New")
            except IncidentStatus.DoesNotExist:
                incident.status = None

            assigned_user = None

            if incident.department:
                responder_profile = DepartmentProfile.objects.filter(
                    department=incident.department,
                    role__name="Responder",
                    is_active=True,
                    is_deleted=False
                ).first()
                if responder_profile:
                    assigned_user = responder_profile.user

            if not assigned_user and incident.division:
                reviewer_profile = DepartmentProfile.objects.filter(
                    division=incident.division,
                    department__isnull=True,
                    role__name="Reviewer",
                    is_active=True,
                    is_deleted=False
                ).first()
                if reviewer_profile:
                    assigned_user = reviewer_profile.user


            if not assigned_user:
                admin_profile = DepartmentProfile.objects.filter(
                    role__name="Admin",
                    is_active=True,
                    is_deleted=False,
                    division__isnull=True,
                    department__isnull=True
                ).first()
                if admin_profile:
                    assigned_user = admin_profile.user

            incident.assigned_to = assigned_user
            incident.save()

            files = request.FILES.getlist('file')
            for f in files:
                IncidentAttachment.objects.create(incident=incident, file=f)


            if incident.email:
                try:
                    send_mail(
                        subject="Your Incident Token",
                        message=f"Thank you for reporting. Your incident token is: {incident.incident_token}",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[incident.email],
                    )
                except Exception as e:
                    print("Failed to send email:", e)
                    
            for key, value in request.POST.items():
                if key.startswith('question_'):
                    question_id = key.split('_')[1]
                    try:
                        question = IncidentQuestion.objects.get(id=question_id)
                        IncidentAnswer.objects.create(
                            incident=incident,
                            question=question,
                            answer_text=value
                        )
                    except IncidentQuestion.DoesNotExist:
                        pass

            return redirect('incident_success', token=incident.incident_token)
        else:
            selected_department_id = request.POST.get('department')
            questions = IncidentQuestion.objects.filter(department_id=selected_department_id) if selected_department_id else []
            return render(request, 'submit_incident.html', {
                'form': form,
                'questions': questions
            })
    else:
        form = IncidentForm()
        selected_department_id = request.GET.get('department')
        questions = IncidentQuestion.objects.filter(department_id=selected_department_id) if selected_department_id else []

        return render(request, 'submit_incident.html', {'form': form,'questions': questions})



def incident_success(request, token):
    incident = get_object_or_404(Incident, incident_token=token, is_deleted=False)
    return render(request, 'incident_confirm.html', {'token': incident.incident_token,'email': incident.email,})



def load_department_questions(request):
    department_id = request.GET.get('department_id')
    questions = IncidentQuestion.objects.filter(department_id=department_id,is_required=True) if department_id else []
    html = render_to_string('dynamic_questions.html', {'questions': questions})
    return JsonResponse({'html': html})

