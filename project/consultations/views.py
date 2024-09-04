from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Specialist, Schedule
from .serializers import SpecialistSerializer, ScheduleSerializer


# Create your views here.
class TestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        Response({'key': 'hello!'})


class ListView(ListAPIView):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer


class SpecialistScheduleView(APIView):
    def get(self, request, pk):
        specialist = Specialist.objects.get(pk=pk)
        return Response({'hello': 'from test'})
        return Response()
