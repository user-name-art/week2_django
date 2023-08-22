import datetime

from django.utils import timezone


def get_duration(visit):
    if not visit.leaved_at:
        return timezone.localtime() - timezone.localtime(visit.entered_at)
    
    return timezone.localtime(visit.leaved_at) - timezone.localtime(visit.entered_at)


def format_duration(duration):
    seconds = duration.total_seconds()
    return f'{int(seconds // 3600)} ч {int((seconds % 3600) // 60)} м'


def is_visit_long(visit):
    visit_time = get_duration(visit)
    return visit_time > datetime.timedelta(hours=1)
