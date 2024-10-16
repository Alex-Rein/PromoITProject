from datetime import datetime

from django.contrib.auth.models import Group, User
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, GenericAPIView

from .models import Specialist, Schedule, Slot, Appointment
from .serializers import (SpecialistSerializer, ScheduleDisplaySerializer, SpecialistRegisterSerializer,
                          ScheduleCreateSerializer, SlotCreateSerializer,
                          AppointmentCreateSerializer, AppointmentCancelSerializer,
                          AdminUserSerializer, AdminUserActionSerializer)
from .permissions import IsNotBlocked, IsSpecialist


# Create your views here.
class SpecialistRegisterView(CreateAPIView):
    """
    POST Регистрация пользователя как специалиста.
    """
    queryset = Specialist.objects.all()
    serializer_class = SpecialistRegisterSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        specialist = Specialist.objects.filter(user=user)
        if specialist.exists():
            return Response({'message': f'Вы уже зарегестрированы по специальности {specialist.first().speciality}.'})

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            spec_group = Group.objects.get(name='Specialist')
            spec_group.user_set.add(user)
            user_group = Group.objects.get(name='User')
            user_group.user_set.remove(user)

            return Response({'message': f'Вы успешно зарегестрированы'
                                        f' по специальности {serializer.data['speciality']}.'})


class SpecialistsListView(ListAPIView):
    """
    GET Список всех специалистов.
    """
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer


class SpecialistDetailView(APIView):
    """
    GET Детальное расписание специалиста для пользователей.
    """

    def get(self, request, pk):
        try:
            specialist = Specialist.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = Schedule.objects.filter(specialist=specialist).filter(date__gte=datetime.today())
        # data = Schedule.objects.filter(specialist=specialist)  # DEBUG отображение всех расписаний
        serializer = ScheduleDisplaySerializer(data, many=True)
        return Response(serializer.data)


class SpecialistScheduleCreateView(CreateAPIView):
    """
    POST Создание расписания специалистом.
    """
    permission_classes = [IsSpecialist, IsNotBlocked]
    serializer_class = ScheduleCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            schedule = serializer.save(user=request.user)
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Расписание создано',
                'id': schedule.id
            })
        else:
            return Response({
                'message': serializer.errors,
            })


class SpecialistScheduleView(ListAPIView):
    """
    GET Просмотр специалистом своего расписания.
    """
    permission_classes = [IsSpecialist, IsNotBlocked]
    serializer_class = ScheduleDisplaySerializer

    def get_queryset(self):
        try:
            specialist = Specialist.objects.get(user=self.request.user)
        except:
            return Specialist.objects.none()

        queryset = Schedule.objects.filter(specialist=specialist)
        return queryset


class SlotCreateView(CreateAPIView):
    """
    POST Создать слот для расписания по его pk.
    """
    permission_classes = [IsSpecialist, IsNotBlocked]
    serializer_class = SlotCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        schedule = Schedule.objects.get(pk=kwargs['pk'])
        if not request.user == schedule.specialist.user:  # Проверка что добавляем слот в свое расписание
            return Response({
                'message': 'Ошибка: У вас нет прав добавлять слот в этом расписании.',
            })

        if serializer.is_valid():
            slot = serializer.save(pk=kwargs['pk'])
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Слот создан',
                'id': slot.id
            })
        else:
            print(serializer.errors)
            return Response({
                'message': serializer.errors,
            })


class AppointmentCreateView(CreateAPIView):
    """
    POST Запись на прием.
    """
    serializer_class = AppointmentCreateSerializer
    queryset = Appointment.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            instance = Slot.objects.get(pk=kwargs['pk'])
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            appointment = serializer.save(pk=kwargs['pk'])
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Запись спрошла успешно',
                'id': appointment.id
            })
        else:
            return Response({
                'message': serializer.errors,
            })


class AppointmentCancelView(UpdateAPIView):
    """
    UPDATE Отменить запись на прием.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentCancelSerializer


class AdminUserListView(ListAPIView):
    """
    GET Список всех пользователей для администратора.
    """
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer


class AdminUserActionView(GenericAPIView):
    """
    POST Управление блокировкой пользователя.
    """
    permission_classes = [IsAdminUser]
    serializer_class = AdminUserActionSerializer

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        blocked_group = Group.objects.get(name='Blocked')
        if not request.user.groups.filter(name='Blocked').exists():
            if request.data['action'] == 'block':
                blocked_group.user_set.add(user)
                return Response({
                    'status': status.HTTP_200_OK,
                    'message': f'Пользователь {user.username} заблокирован'
                })
            elif request.data['action'] == 'unblock':
                blocked_group.user_set.remove(user)
                return Response({
                    'status': status.HTTP_200_OK,
                    'message': f'Пользователь {user.username} разблокирован'
                })
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': serializer.errors
            })
