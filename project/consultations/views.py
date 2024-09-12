from datetime import datetime

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

from .models import Specialist, Schedule, Slot, Appointment
from .serializers import (SpecialistSerializer, ScheduleDisplaySerializer,
                          ScheduleCreateSerializer, SlotDisplaySerializer,
                          SlotCreateSerializer, AppointmentCreateSerializer)
from .permissions import CustomModelPermission


# Create your views here.
class TestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'key': 'hello!'})


class SpecialistsListView(ListAPIView):
    """
    GET Список всех специалистов.
    """
    # permission_classes = [CustomModelPermission]  # TODO вернуть в рабочку
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer


class SpecialistDetailView(APIView):
    """
    GET Детальное расписание специалиста для пользователей.
    """
    # permission_classes = [CustomModelPermission]  # TODO вернуть в рабочку

    def get(self, request, pk):
        try:
            specialist = Specialist.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # data = Schedule.objects.filter(specialist=specialist).filter(date__gte=datetime.today())  # TODO вернуть в рабочку
        data = Schedule.objects.filter(specialist=specialist)
        serializer = ScheduleDisplaySerializer(data, many=True)
        return Response(serializer.data)


class SpecialistScheduleCreateView(CreateAPIView):
    """
    POST Создание расписания специалистом.
    """
    # permission_classes = [IsAuthenticated]  # TODO redo permissions
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
            print(serializer.errors)
            return Response({
                'message': serializer.errors,
            })


class SpecialistScheduleView(ListAPIView):
    """
    GET Просмотр специалистом своего расписания.
    """
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
    # permission_classes = [CustomModelPermission]  # TODO вернуть в рабочку
    serializer_class = SlotCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

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


class SlotDetailView(RetrieveAPIView):
    # permission_classes = [CustomModelPermission]  # TODO вернуть в рабочку
    queryset = Slot.objects.all()
    serializer_class = SlotDisplaySerializer


class AppointmentCreateView(CreateAPIView):
    """
    POST Запись на прием.
    """
    # permission_classes = [CustomModelPermission]  # TODO вернуть в рабочку
    serializer_class = AppointmentCreateSerializer
    queryset = Appointment.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            instance = Slot.objects.get(pk=kwargs['pk'])
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if instance.status == Slot.Statuses.RESERVED:
            return Response({
                'message': 'Запись не прошла. Слот занят'
            })

        if serializer.is_valid():
            appointment = serializer.save(pk=kwargs['pk'], user=request.user)
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Запись спрошла успешно',
                'id': appointment.id
            })
        else:
            print(serializer.errors)
            return Response({
                'message': serializer.errors,
            })
