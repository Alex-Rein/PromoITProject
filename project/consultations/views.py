from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Specialist
from .serializers import SpecialistSerializer, SpecialistScheduleSerializer
from .permissions import CustomModelPermission


# Create your views here.
class TestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'key': 'hello!'})


class ListView(ListAPIView):
    # permission_classes = [CustomModelPermission]
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer


class SpecialistScheduleView(RetrieveAPIView):
    # permission_classes = [CustomModelPermission]
    queryset = Specialist.objects.all()
    serializer_class = SpecialistScheduleSerializer


# class SpecialistScheduleView(APIView):
#     permission_classes = [CustomObjectPermission]
#
#     def get(self, request, pk):
#         specialist = Specialist.objects.get(pk=pk)
#         serializer = SpecialistScheduleSerializer(specialist)
#         return Response(serializer.data)
