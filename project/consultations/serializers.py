from datetime import datetime, timedelta

from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Specialist, Schedule, Slot, Appointment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class AdminUserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'groups')


class AdminUserActionSerializer(serializers.Serializer):
    actions = {
        ('block', 'Заблокировать'),
        ('unblock', 'Разблокировать')
    }
    action = serializers.ChoiceField(actions, required=True)

    class Meta:
        fields = ('action',)


class SlotDisplaySerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Slot
        fields = ('id', 'start_time', 'end_time', 'status', 'context')


class SlotCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ('start_time', 'duration', 'context', 'reserved_for_user')
        # exclude = ('status', 'end_time', 'schedule')

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

    def validate(self, data):
        """
        Проверка ввода длительности приема.
        """
        duration = data.get('duration')
        if duration:
            if duration < 15:
                raise serializers.ValidationError({'message': 'Ошибка: Время приема не должно быть меньше 15 минут.'})
            elif duration > 120:
                raise serializers.ValidationError({'message': 'Ошибка: Время приема не должно превышать 120 минут.'})

        return data


class ScheduleDisplaySerializer(serializers.ModelSerializer):
    slots = SlotDisplaySerializer(allow_null=True, many=True, required=False)

    class Meta:
        model = Schedule
        fields = ('id', 'date', 'work_shift_start_time', 'work_shift_end_time', 'slots')


class ScheduleCreateSerializer(serializers.ModelSerializer):
    date = serializers.DateField()

    class Meta:
        model = Schedule
        fields = ('date', 'work_shift_start_time', 'work_shift_end_time')

    def save(self, **kwargs):
        if self.is_valid():
            specialist = Specialist.objects.get(user=kwargs['user'])
            schedule = Schedule.objects.create(
                **self.validated_data,
                specialist=specialist,
            )
            schedule.save()

            return schedule

    def validate(self, data):
        """
        Проверка даты, начала и конца рабочего времени.
        """
        start_time = data.get('work_shift_start_time')
        end_time = data.get('work_shift_end_time')
        start_time_obj = datetime.strptime(str(start_time), '%H:%M:%S')
        end_time_obj = datetime.strptime(str(end_time), '%H:%M:%S')
        if (end_time_obj - start_time_obj) < timedelta(minutes=15):
            raise serializers.ValidationError('Рабочее время не должно быть короче 1 приема (15 минут).')
        elif (end_time_obj - start_time_obj) > timedelta(hours=8):
            raise serializers.ValidationError('Рабочее время не должно превышать 8 часов.')

        date = data.get('date')
        date_now = datetime.now().date()
        if date < date_now:
            raise serializers.ValidationError('Дата расписания указана не верно.')

        return data


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
            user = self.context['request'].user
            slot = Slot.objects.get(pk=kwargs['pk'])

            if slot.status == Slot.Statuses.RESERVED:  # Проверка доступности слота
                raise serializers.ValidationError({
                            'message': 'Запись не прошла т.к. слот уже занят.'
                        })

            appointment = Appointment.objects.create(
                user=user,
                slot=slot
            )
            slot.reserved_for_user = user
            slot.status = Slot.Statuses.RESERVED
            slot.save()

            return appointment


class AppointmentCancelSerializer(serializers.ModelSerializer):
    slot_id = serializers.CharField(source='slot.pk', read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Appointment
        fields = ('cancel_cause_choice', 'cancel_cause', 'slot_id', 'status')

    def update(self, instance, validated_data):
        slot = instance.slot
        slot.reserved_for_user = None
        slot.status = Slot.Statuses.FREE
        slot.save()

        appointment = instance
        appointment.cancel_cause = validated_data.get('cancel_cause')
        appointment.cancel_cause_choice = validated_data.get('cancel_cause_choice')
        appointment.save()
        return appointment

    def validate(self, data):
        """
        Проверка что у пользователя есть доступ для отмены и что указана причина отмены записи.
        """
        if self.instance:
            reserved_for_user = self.instance.slot.reserved_for_user
            user = self.context['request'].user
            if user == reserved_for_user:  # Проверяем что мы отменяем свою запись.
                cancel_cause_choice = data.get('cancel_cause_choice')
                cancel_cause = data.get('cancel_cause')
                if not cancel_cause_choice and not cancel_cause:
                    raise serializers.ValidationError("Пожалуйста выберите причину отмены записи"
                                                      " на консультацию или укажите свою.")
            else:
                raise serializers.ValidationError("Запись уже отменена или у вас не хватает для этого прав.")
        return data


class SpecialistSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Specialist
        fields = ('id', 'speciality', 'user', 'is_on_vacation')


class SpecialistRegisterSerializer(serializers.ModelSerializer):
    speciality = serializers.CharField(required=True)

    class Meta:
        model = Specialist
        fields = ('speciality',)

    def save(self, **kwargs):
        if self.is_valid():
            Specialist.objects.create(
                **self.validated_data,
                user=kwargs['user'],
            )
