from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Appointment(models.Model):
    class CancelCauses(models.TextChoices):
        CAUSE1 = 'c1', 'Причина1'
        CAUSE2 = 'c2', 'Причина2'
        CAUSE3 = 'c3', 'Причина3'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cancel_cause_choice = models.CharField(choices=CancelCauses, max_length=2, null=True, blank=True)
    cancel_cause = models.TextField(blank=True, null=True)


class Slot(models.Model):
    class Statuses(models.TextChoices):
        FREE = 'fr', 'Свободно'
        RESERVED = 're', 'Забронировано'

    status = models.CharField(choices=Statuses, max_length=2, default=Statuses.FREE)
    time = models.TimeField()
    duration = models.IntegerField(default=60, blank=True)
    context = models.TextField(blank=True, null=True)
    reserved_for_user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    appointments = models.ForeignKey(Appointment, on_delete=models.CASCADE)


class Schedule(models.Model):
    date = models.DateField()
    work_shift_start_time = models.TimeField()
    work_shift_end_time = models.TimeField()
    slots = models.ForeignKey(Slot, on_delete=models.CASCADE)


class Specialist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    schedules = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    is_on_vacation = models.BooleanField(default=False)

