from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from django.contrib.auth.models import User

from .models import Specialist, Schedule, Slot, Appointment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class ScheduleListSerializer(WritableNestedModelSerializer):
    schedule = ScheduleSerializer(many=True, required=False)

    class Meta:
        model = Schedule


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class SpecialistSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Specialist
        fields = ('id', 'speciality', 'user')
