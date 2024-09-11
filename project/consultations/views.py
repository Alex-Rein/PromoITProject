from datetime import datetime
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Specialist, Schedule
from .serializers import SpecialistSerializer, ScheduleSerializer, SlotDisplaySerializer, SlotCreateSerializer
from .permissions import CustomModelPermission


# Create your views here.
class TestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'key': 'hello!'})


class ListView(ListAPIView):
    """
    Список специалистов
    """
    # permission_classes = [CustomModelPermission]
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer


# class SpecialistScheduleView(RetrieveAPIView):
#     permission_classes = [CustomModelPermission]
#     queryset = Specialist.objects.all()
#     serializer_class = SpecialistScheduleSerializer


class SpecialistScheduleView(APIView):
    """
    Расписание специалиста
    """
    # permission_classes = [CustomModelPermission]

    def get(self, request, pk):
        specialist = Specialist.objects.get(pk=pk)
        # data = Schedule.objects.filter(specialist=specialist).filter(date__gte=datetime.today())
        data = Schedule.objects.filter(specialist=specialist)
        serializer = ScheduleSerializer(data, many=True)
        return Response(serializer.data)


class SlotCreateView(viewsets.ModelViewSet):
    serializer_class = SlotCreateSerializer
    http_method_names = ['post', 'patch']

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
            print(print(serializer.errors))
            return Response({
                'message': serializer.errors,
            })
