from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView, DetailView, TemplateView
from django.views.decorators.cache import cache_page
from django.db.models import Q
from bus_tracker.models import Light, BusStop, BusRoute, BusLocation, Bus, ArrivalTime, Direction
from django import forms
from gmapi import maps
from gmapi.forms.widgets import GoogleMap
from django_twilio.client import twilio_client
from bus_tracker.serializers import LightSerializer, BusLocationSerializer, BusStopSerializer
from rest_framework import generics
from rest_framework.response import Response
import math
def sms(request):
	textmessage = request.GET.get('Body', '')
	sender = request.GET.get('From', '')
	if textmessage:
		splitmessage = textmessage.split(';')
		#messages should arrive in the form of lat;loni
		bus = Bus.objects.get(phone_number=sender)
		updatelocation = BusLocation.objects.get(bus=bus)
		updatelocation.lat = splitmessage[0]
		updatelocation.lon = splitmessage[1]
		messagetostops = splitmessage[0]+";"+splitmessage[1]
		stops = BusStop.objects.filter(routes=bus.bus_route)
#		twilio_client.sms.messages.create(to="+12502086479", from_="+12509842369", body=messagetostops)
		for stop in stops:
			twilio_client.sms.messages.create(to=stop.phone_number, from_="+12509842369", body=messagetostops)
		updatelocation.save()

	return render_to_response("bus_tracker/default.html", RequestContext(request))

class MapForm(forms.Form):
	map = forms.Field(widget=GoogleMap(attrs={'width':510, 'height':510}))

def displayroute(request, pk, direction="East"):
	route = BusRoute.objects.get(id=pk)
	try:
		bus = Bus.objects.get(bus_route=route)
		buslocation = BusLocation.objects.get(bus=bus)
	except:
		bus = Bus.objects.get(id=1)
		buslocation = BusLocation.objects.get(bus=bus)

	direct = Direction.objects.get(name=direction)
	nonedirect = Direction.objects.get(name="None")
	stops = BusStop.objects.filter(routes=route,direction=direct)
	times2 = ArrivalTime.objects.filter(route=route)
	times = []
	for time in times2:
		times.append(time.time)
	stops = BusStop.objects.filter(routes=route, direction=direct)
	nonestops = BusStop.objects.filter(routes=route, direction=nonedirect)
	lat = buslocation.lat
	lon = buslocation.lon
	gmap = maps.Map(opts = {
		'center': maps.LatLng(lat, lon),
		'mapTypeId': maps.MapTypeId.ROADMAP,
		'zoom': 13,
		'mapTypeControlOptions': {
			'style': maps.MapTypeControlStyle.DROPDOWN_MENU
		},
	})
	for stop in nonestops:
		marker = maps.Marker(opts = {
			'map': gmap,
			'position': maps.LatLng(stop.lat, stop.lon),
		})
	for stop in stops:
		marker = maps.Marker(opts = {
			'map': gmap,
			'position': maps.LatLng(stop.lat, stop.lon),
		})
	marker2 = maps.Marker(opts = {
		'map': gmap,
		'position': maps.LatLng(lat, lon),
	})
	maps.event.addListener(marker2, 'mouseover', 'myobj.markerOver')
	maps.event.addListener(marker2, 'mouseout', 'myobj.markerOut')
	info = maps.InfoWindow({
		'content': 'Current Bus Location',
		'disableAutoPan': True
	})
	info.open(gmap, marker2)	

	context = {'form': MapForm(initial={'map':gmap}), 'busroute': route, 'nonestops': nonestops, 'times': times, 'stops': stops}
	return render_to_response("bus_tracker/busroute_detail.html", context, RequestContext(request))

class BusLocationDetail(generics.RetrieveAPIView):
	model = BusLocation
	serializer_class = BusLocationSerializer
	def get(self, request, bus, format=None):
		ourbus = Bus.objects.get(id_number=bus)
		buslocation = BusLocation.objects.get(bus=ourbus)
		serializer = BusLocationSerializer(buslocation)
		return Response(serializer.data)


class BusStopDetail(generics.RetrieveAPIView):
	model = BusStop
	serializer_class = BusStopSerializer
	def get(self, request, route, format=None):
		our_route = BusRoute.objects.get(route_short_name=route)
		bus_stops = BusStop.objects.filter(routes=our_route)
		serializer = BusStopSerializer(bus_stops)
		return Response(serializer.data)

class LightDetail(generics.RetrieveAPIView):
	model = Light
	serializer_class = BusStopSerializer
	def get(self, request, route, bus, format=None):
		our_bus = Bus.objects.get(id_number=bus)
		bus_location = BusLocation.objects.get(bus=our_bus)
		our_route = BusRoute.objects.get(route_short_name=route)
		bus_stops = BusStop.objects.filter(routes=our_route)
		current_distance = 10000
		for stop in bus_stops:
			distance = distance_on_unit_sphere(bus_location.lat, bus_location.lon, stop.lat, stop.lon)
			if distance < current_distance:
				current_distance = distance
				closest_stop = stop
		bus_light = Light.objects.get(stop = closest_stop)
		serializer = LightSerializer(bus_light)
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
