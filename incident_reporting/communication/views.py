from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localtime
from django.http import JsonResponse
from .models import Incident, IncidentMessage

@login_required
def incident_chat_view(request, incident_id):
    incident = get_object_or_404(Incident, id=incident_id)

    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        message = request.POST.get("message")
        is_internal = request.POST.get("is_internal") == "on"

        if message:
            new_msg = IncidentMessage.objects.create(
                incident=incident,
                sender=request.user,
                message=message,
                is_internal=is_internal
            )
            return JsonResponse({
                "success": True,
                "message": new_msg.message,
                "created_at": localtime(new_msg.created_at).strftime("%d %b %Y, %H:%M"),
                "sender_name": new_msg.sender.fullname if new_msg.sender else "Anonymous",
                "is_internal": new_msg.is_internal
            })

        return JsonResponse({"success": False, "error": "Message is empty"})

    messages = incident.messages.select_related("sender").order_by("created_at")

    return render(request, "chat.html", {
        "incident": incident,
        "messages": messages
    })


