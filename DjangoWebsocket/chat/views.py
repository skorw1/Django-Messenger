import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
from .models import UserActivity
# Create your views here.
@login_required
def index(request):
    return render(request, 'chat/index.html')
@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


def activity_report(request):
    activities = UserActivity.objects.all().order_by('-timestamp')
    return render(request, 'chat/activity_report.html', {'activities': activities})