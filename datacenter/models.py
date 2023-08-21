from django.db import models
from django.utils import timezone

import datetime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


def get_duration(visit):
    if not visit.leaved_at:
        return timezone.localtime() - timezone.localtime(visit.entered_at)
    else:
        return timezone.localtime(visit.leaved_at) - timezone.localtime(visit.entered_at)


def format_duration(duration):
    seconds = duration.total_seconds()
    return f'{int(seconds // 3600)} ч {int((seconds % 3600) // 60)} м'


def is_visit_long(visit):
    visit_time = get_duration(visit)
    if visit_time > datetime.timedelta(hours=1):
        return True
    else:
        return False

