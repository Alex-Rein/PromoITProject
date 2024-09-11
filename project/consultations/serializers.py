from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from django.contrib.auth.models import User

from .models import Specialist, Schedule, Slot, Appointment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class SlotSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Slot
        fields = ('id', 'start_time', 'status', 'duration', 'context')

    def create(self, validated_data):
        return Slot.objects.create(**validated_data)

    def update(self, instance, validated_data):
        ...


class ScheduleSerializer(WritableNestedModelSerializer):
    slots = SlotSerializer(allow_null=True, many=True, required=False)

    class Meta:
        model = Schedule
        fields = ('id', 'date', 'work_shift_start_time', 'work_shift_end_time', 'slots')


# class SpecialistScheduleSerializer(WritableNestedModelSerializer):
#     schedules = ScheduleSerializer(allow_null=True, many=True, required=False)
#
#     class Meta:
#         model = Specialist
#         fields = ('schedules', )


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class SpecialistSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Specialist
        fields = ('id', 'speciality', 'user')
