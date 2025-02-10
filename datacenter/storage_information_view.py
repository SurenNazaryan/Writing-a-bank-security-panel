from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_duration, format_duration
from django.utils.timezone import localtime


def storage_information_view(request):
    non_closed_visits = []
    non_closed_visits_objects = Visit.objects.filter(leaved_at__isnull=True)
    for visit in non_closed_visits_objects:
        duration = get_duration(visit)
        non_closed_visits.append(
            {
                'who_entered': visit.passcard.owner_name,
                'entered_at': localtime(visit.entered_at),
                'duration': format_duration(duration),
            }
        )
    context = {
        'non_closed_visits': non_closed_visits
    }
    return render(request, 'storage_information.html', context)
