from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView, DetailView, TemplateView
from django.views.decorators.cache import cache_page
from django.db.models import Q
from gtfs_bus.models import *
from gtfs_bus.serializers import BusSerializer
from django import forms
from gmapi import maps
from gmapi.forms.widgets import GoogleMap
from django_twilio.client import twilio_client
from rest_framework import generics
from rest_framework.response import Response
import math

class MapForm(forms.Form):
	map = forms.Field(widget=GoogleMap(attrs={'width':510, 'height':510}))

def displayroute(request, pk):
	route = Route.objects.get(id=pk)

class BusDetail(generics.RetrieveAPIView):
	model = Bus
	serializer_class = BusSerializer
	def get(self, request, route, format=None):
		bus_list = []
		our_route = Route.objects.get(route_shortname = route)
		our_trips = Trip.objects.filter(route = our_route)
		for trips in our_trips:
			try:
				bus_list += Bus.objects.filter(trip = trips)
			except:
				pass
		serializer = BusSerializer(bus_list)
		return Response(serializer.data)
 
