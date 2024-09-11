from datetime import datetime, timedelta

from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from django.contrib.auth.models import User

from .models import Specialist, Schedule, Slot, Appointment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class SlotDisplaySerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Slot
        fields = ('id', 'start_time', 'end_time', 'status', 'context')


class SlotCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        exclude = ('status', 'end_time', 'schedule')

    def save(self, **kwargs):
        if self.is_valid():
            start_time = self.validated_data.get('start_time')
            time_obj = datetime.strptime(str(start_time), '%H:%M:%S')
            duration = self.validated_data.get('duration')
            if duration:
                end_time = time_obj + timedelta(minutes=duration)
            else:
                end_time = time_obj + timedelta(hours=1)

            slot = Slot.objects.create(
                **self.validated_data,
                end_time=end_time,
                schedule=Schedule.objects.get(pk=kwargs['pk']),
                status=Slot.Statuses.RESERVED if self.validated_data.get('reserved_for_user')
                else Slot.Statuses.FREE
            )
            return slot


class ScheduleDisplaySerializer(WritableNestedModelSerializer):
    slots = SlotDisplaySerializer(allow_null=True, many=True, required=False)

    class Meta:
        model = Schedule
        fields = ('id', 'date', 'work_shift_start_time', 'work_shift_end_time', 'slots')


class AppointmentDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ()

    def save(self, **kwargs):
        if self.is_valid():
            slot = Slot.objects.get(pk=kwargs['pk'])

            appointment = Appointment.objects.create(
                user=kwargs['user'],
                slot=slot
            )
            slot.reserved_for_user = kwargs['user']
            slot.status = Slot.Statuses.RESERVED
            slot.save()

            return appointment


class SpecialistSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Specialist
        fields = ('id', 'speciality', 'user')
