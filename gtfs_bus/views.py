from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView, DetailView, TemplateView
from django.views.decorators.cache import cache_page
from django.db.models import Q
from gtfs_bus.models import *
from gtfs_bus.serializers import *
from django import forms
from time import time
from datetime import datetime
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

def display_route(request, pk, dow="Weekday"):
	direction = request.GET.get('dir', '')
	route = Route.objects.get(route_shortname=pk)
	if direction:
		trips = Trip.objects.filter(route=route, day=dow, headsign = direction)
	else:
		trips = Trip.objects.filter(route=route, day=dow)
	busses = Bus.objects.filter(trip__in = trips)
	stops = Stops.objects.filter(~Q(light_num=0))
	stop_times = StopTimes.objects.filter(trip__in = trips, stop__in = stops).order_by('trip', 'stop_sequence')
	try:
		gmap = maps.Map(opts = {
			'center': maps.LatLng(busses[0].lat, busses[0].lon),
			'mapTypeId': maps.MapTypeId.ROADMAP,
			'zoom': 13,
			'mapTypeControlOptions': {
				'style': maps.MapTypeControlStyle.DROPDOWN_MENU
			},
		})
	except:
		gmap = maps.Map(opts = {
			'center': maps.LatLng(stops[0].lat, stops[0].lon),
			'mapTypeId': maps.MapTypeId.ROADMAP,
			'zoom': 13,
			'mapTypeControlOptions': {
				'style': maps.MapTypeControlStyle.DROPDOWN_MENU
			},
		})
		
	for stoptime in stop_times:
		marker = maps.Marker(opts = {
			'map': gmap,
			'position': maps.LatLng(stoptime.stop.lat, stoptime.stop.lon),
		})
	for bus in busses:
		marker2 = maps.Marker(opts = {
			'map': gmap,
			'position': maps.LatLng(bus.lat, bus.lon),
		})
		maps.event.addListener(marker2, 'mouseover', 'myobj.markerOver')
		maps.event.addListener(marker2, 'mouseout', 'myobj.markerOut')
		info = maps.InfoWindow({
			'content': 'TripID: ' + str(bus.trip.trip_id),
			'disableAutoPan': True
		})
		info.open(gmap, marker2)
	context = {'trips': trips, 'stops': stops, 'form': MapForm(initial={'map':gmap}), 'busroute':route, 'stop_times':stop_times}
	return render_to_response("gtfs_bus/route_detail.html", context, RequestContext(request))

	
#API Calls
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

class ScheduleDetail(generics.RetrieveAPIView):
	model = StopTimes
	serializer_class = StopTimesSerializer
	def get(self, request, route, format=None):
		our_route = Route.objects.get(route_shortname = route)
		our_trips = Trip.objects.filter(route=our_route)
		stop_times = StopTimes.objects.filter(trip__in = our_trips).order_by('trip', 'stop_sequence')
		serializer = StopTimesSerializer(stop_times)
		return Response(serializer.data)

class NextStopTime(generics.RetrieveAPIView):
	model = StopTimes
	serializer_class = StopTimesSerializer
	def get(self, request, trip_id, stop_id, format=None):
		our_trip = Trip.objects.get(trip_id=trip_id)
		stop_times = StopTimes.objects.filter(trip = our_trip)
		hour = datetime.now().hour
		next_stop = stop_times[0]
		minutes = datetime.now().minute
		h_curr = 23
		m_curr = 59
		for stop in stop_times:
			arrival_time = str(stop.arrival_time)
			split_time = arrival_time.split(':')
			h_diff = int(split_time[0]) - int(hour)
			m_diff = int(split_time[1]) - int(minutes)
			if h_diff > -1 and m_diff > -1:
				if h_diff < h_curr:
					if m_diff < m_curr:
						m_curr = m_diff
						h_curr = h_diff
						next_stop = stop
		serializer = StopTimesSerializer(next_stop)
		return Response(serializer.data)


class LightDetail(generics.RetrieveAPIView):
	model = Stops
	serializer_class = StopsSerializer
	def get(self, request, route, format=None):
		stops_final = []
		our_route = Route.objects.get(route_shortname = route)
		our_trips = Trip.objects.filter(route=our_route)
		our_bus = Bus.objects.filter(trip__in = our_trips)
		our_stops = Stops.objects.filter(~Q(light_num=0))
		stop_dict = {}
		bus_dict = {}
		for bus in our_bus:
			bus_dict[bus] = 10000
		for stop in our_stops:
			for bus in our_bus:
				distance = distance_on_unit_sphere(stop.lat, stop.lon, bus.lat, bus.lon)
				if bus_dict[bus] > distance:
					bus_dict[bus] = distance
					stop_dict[bus.id] = stop.id
		for key in stop_dict:
			stops_final += Stops.objects.filter(id = stop_dict[key])
		serializer = StopsSerializer(stops_final)
		return Response(serializer.data)
			
			


def distance_on_unit_sphere(lat1, long1, lat2, long2):
	# Convert latitude and longitude to
	# spherical coordinates in radians.
	degrees_to_radians = math.pi/180.0
	# phi = 90 - latitude
	phi1 = (90.0 - float(lat1))*degrees_to_radians
	phi2 = (90.0 - float(lat2))*degrees_to_radians
	# theta = longitude
	theta1 = float(long1)*degrees_to_radians
	theta2 = float(long2)*degrees_to_radians
	# Compute spherical distance from spherical coordinates.
	# For two locations in spherical coordinates
	# (1, theta, phi) and (1, theta, phi)
	# cosine( arc length ) =
	#    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
	# distance = rho * arc length
	cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + math.cos(phi1)*math.cos(phi2))
	arc = math.acos( cos )
	# Remember to multiply arc by the radius of the earth
	# in your favorite set of units to get length.
	return arc




