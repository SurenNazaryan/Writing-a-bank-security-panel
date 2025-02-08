from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render, get_object_or_404
from datacenter.models import get_duration, format_duration, is_visit_long


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []
    for visit in visits:
        entered_at = visit.entered_at
        duration = get_duration(visit)
        formated_duration = format_duration(duration)
        is_strange = is_visit_long(visit, minutes=60)
        this_passcard_visits.append(
            {
                'entered_at': entered_at,
                'duration': formated_duration,
                'is_strange': is_strange
            },
        )
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
