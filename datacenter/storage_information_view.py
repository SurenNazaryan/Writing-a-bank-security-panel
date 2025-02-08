from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_duration, format_duration
from django.utils import timezone


def storage_information_view(request):
    non_closed_visits = []
    non_closed_visits_objects = Visit.objects.filter(leaved_at__isnull=True)
    for visit in non_closed_visits_objects:
        who_entered = visit.passcard.owner_name
        visit_local_time = timezone.localtime(visit.entered_at)
        duration = get_duration(visit)
        formated_duration = format_duration(duration)
        non_closed_visits.append(
            {
                'who_entered': who_entered,
                'entered_at': visit_local_time,
                'duration': formated_duration,
            }
        )
    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
