from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Incident, IncidentMessage

@login_required
def incident_chat_view(request, incident_id):
    incident = get_object_or_404(Incident, id=incident_id)
    messages = incident.messages.select_related('sender').order_by('created_at')

    return render(request, 'chat.html', {
        'incident_details': incident,
        'messages': messages,
    })

@login_required
@csrf_exempt
def post_chat_message(request, incident_id):
    if request.method == "POST":
        message_text = request.POST.get("message", "").strip()
        is_internal = request.POST.get("is_internal") == "true"

        if not message_text:
            return JsonResponse({"success": False, "error": "Message is empty"}, status=400)

        try:
            incident = Incident.objects.get(id=incident_id)
        except Incident.DoesNotExist:
            return JsonResponse({"success": False, "error": "Incident not found"}, status=404)

        msg = IncidentMessage.objects.create(
            incident=incident,
            sender=request.user,
            message=message_text,
            is_internal=is_internal,
            created_at=timezone.now()
        )

        return JsonResponse({
            "success": True,
            "sender_name": request.user.fullname,
            "message": msg.message,
            "created_at": msg.created_at.strftime("%d %b %Y, %H:%M"),
            "is_internal": msg.is_internal
        })

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)
