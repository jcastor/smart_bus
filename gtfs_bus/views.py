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

def update_location(request):
	textmessage = request.GET.get('Body', '')
	sender = request.GET.get('From', '')
	#http://499.jason-castor.com/gtfs/update/?From=%2B12502086479&Body=U%3B48.1%3B-123.1
	if textmessage:
		if textmessage.startswith("U"): #message should be of the form U;lat;lon
			split = textmessage.split(';')
			bus = Bus.objects.get(phone_num = sender)
			bus.lat = split[1]
			bus.lon = split[2]
			bus.save()
			return render_to_response("gtfs_bus/success.html", RequestContext(request))
		else:
			if sender != "+911":
				twilio_client.sms.messages.create(to=sender, from_="+12509842369", body="")	
	
	return render_to_response("gtfs_bus/default.html", RequestContext(request))

class MapForm(forms.Form):
	map = forms.Field(widget=GoogleMap(attrs={'width':510, 'height':510}))

def display_route(request, pk):
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
 
