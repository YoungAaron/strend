from django.shortcuts import render
from cbond.models import *
from cbond.serializers import *
from rest_framework import generics


class CbondListView(generics.ListCreateAPIView):
    queryset = CbondList.objects.all()
    serializer_class = CbondListSerializer


class CbondDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CbondList.objects.all()
    serializer_class = CbondListSerializer

