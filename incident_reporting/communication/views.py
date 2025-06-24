from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from communication.models import IncidentMessage, IncidentMessageAttachment
from communication.forms import IncidentMessageFormPublic, IncidentMessageAttachmentForm, IncidentMessageFormInternal
from incidents.models import Incident
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

# Create your views here.

def ajax_public_chat(request, token):
    incident = get_object_or_404(Incident, incident_token=token, is_deleted=False)
    messages = incident.messages.filter(is_internal_only=False).order_by('created_at')

    if request.method == 'POST':
        form = IncidentMessageFormPublic(request.POST)
        file_form = IncidentMessageAttachmentForm(request.POST, request.FILES)

        if form.is_valid():
            message = form.save(commit=False)
            message.incident = incident
            message.sender = None
            message.save()

            if file_form.is_valid() and 'file' in request.FILES:
                for f in request.FILES.getlist('file'):
                    IncidentMessageAttachment.objects.create(message=message, file=f)

    else:
        form = IncidentMessageFormPublic()
        file_form = IncidentMessageAttachmentForm()

    html = render_to_string("communication/public_chat_page.html", {
        'incident': incident,
        'messages': messages,
        'form': form,
        'file_form': file_form,
    }, request=request)

    return JsonResponse({'html': html})


@login_required
def ajax_internal_chat(request, token):
    incident = get_object_or_404(Incident, incident_token=token, is_deleted=False)
    messages = incident.messages.all().order_by('created_at')

    if request.method == 'POST':
        form = IncidentMessageFormInternal(request.POST)
        file_form = IncidentMessageAttachmentForm(request.POST, request.FILES)

        if form.is_valid():
            message = form.save(commit=False)
            message.incident = incident
            message.sender = request.user
            message.is_internal_only = form.cleaned_data.get('is_internal_only', False)
            message.save()

            if file_form.is_valid() and 'file' in request.FILES:
                for f in request.FILES.getlist('file'):
                    IncidentMessageAttachment.objects.create(message=message, file=f)
    else:
        form = IncidentMessageFormInternal()
        file_form = IncidentMessageAttachmentForm()

    html = render_to_string("communication/internal_chat_page.html", {
        'incident': incident,
        'messages': messages,
        'form': form,
        'file_form': file_form,
        'user': request.user,
    }, request=request)

    return JsonResponse({'html': html})