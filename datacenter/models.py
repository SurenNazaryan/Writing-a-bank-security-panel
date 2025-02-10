from django.db import models
from django.utils.timezone import localtime


SECONDS_IN_HOUR = 3600
SECONDS_IN_MINUTE = 60


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
    entered_time = localtime(visit.entered_at)
    leaved_time = localtime(visit.leaved_at)
    duration = int((leaved_time - entered_time).total_seconds())
    return duration


def format_duration(duration):
    hours = duration // SECONDS_IN_HOUR
    minutes = (duration % SECONDS_IN_HOUR) // SECONDS_IN_MINUTE
    formated_duration = f'{hours} ч. {minutes} мин.'
    return formated_duration


def is_visit_long(visit, minutes=60):
    duration = get_duration(visit)
    flag = duration > minutes * SECONDS_IN_MINUTE
    return flag
