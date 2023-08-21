from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_duration, format_duration, is_visit_long


def storage_information_view(request):
    active_visits = Passcard.objects.filter(visit__leaved_at=None)

    non_closed_visits = []
    
    employees_in_room = Passcard.objects.filter(visit__leaved_at=None)

    for employee_in_room in employees_in_room:
        employee = Passcard.objects.get(owner_name=employee_in_room.owner_name)
        active_visit = Visit.objects.get(passcard=employee_in_room, leaved_at=None)

        non_closed_visit = {
            'who_entered': employee_in_room.owner_name,
            'entered_at': active_visit.entered_at.strftime('%d-%m-%Y %H:%M'),
            'duration': format_duration(get_duration(active_visit)),
            'is_strange': is_visit_long(active_visit)
        }

        non_closed_visits.append(non_closed_visit)

    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
