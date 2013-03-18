from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView, DetailView, TemplateView
from django.views.decorators.cache import cache_page
from django.db.models import Q
from gtfs_bus.models import *
from gtfs_bus.serializers import *
import gtfs_bus.helpers as helpers
from gtfs_bus.forms import MapForm
from time import time
from datetime import datetime
from datetime import date
from gmapi import maps
from django_twilio.client import twilio_client
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Count

# View: process_sms
# This view will process sms messages, either updating a bus location or sending out
# bus times for a stop
def process_sms(request):
	textmessage = request.GET.get('Body', '')
	calendars = Calendar.objects.all()
	our_calendars = []
	for calendar in calendars:
		if calendar.start_date < date.today() and calendar.end_date > date.today():
			our_calendars += Calendar.objects.filter(service_id = calendar.service_id)
	sender = request.GET.get('From', '')
	final_send = ""
	i = 0 #initialize counter to only return 3 values
	#http://499.jason-castor.com/gtfs/update/?From=%2B12502086479&Body=U%3B48.1%3B-123.1
	if textmessage:
		if textmessage.startswith("U"): #message should be of the form U;lat;lon
			split = textmessage.split(';')
			bus = Bus.objects.get(phone_num = sender)
			bus.lat = split[1] 
			bus.lon = split[2]
			bus.save() #save the bus with the updated coordinates from request
			return render_to_response("gtfs_bus/success.html", RequestContext(request))
		else:
			if sender != "+911": #ideally we dont want to be texting messages to 911
				try:
					stop = Stops.objects.get(stop_id = textmessage) #get the stops by the given stop_id
					day = datetime.now().weekday() #grab the current day of the week
					#grabbing the trips for the day of the week that is now
					if day == 6:
						trips = Trip.objects.filter(day="Sunday", service_id__in = our_calendars)
					elif day == 5:
						trips = Trip.objects.filter(day="Saturday", service_id__in = our_calendars)
					else:
						trips = Trip.objects.filter(day="Weekday", service_id__in = our_calendars)
					#grab our stop times based on trips in our day of week and for the stop_id given order by
					#arrival_time in order to find the next 3 times	
					stop_times = StopTimes.objects.filter(trip__in = trips,stop=stop).order_by('arrival_time')
					hour = datetime.now().hour
					minutes = datetime.now().minute
					for time in stop_times:
						split_time = str(time.arrival_time).split(':') #split the time into hours and minutes
						if i < 3: #check out counter (we only want to return the first 3 results
							if int(split_time[0]) == hour:
								if int(split_time[1]) > minutes:
									i += 1 #if the hour is the same or greater and the minutes are greater we have a valid next stop time
									route_name = time.trip.route.route_shortname
									route_time = time.arrival_time
									#construct our string we will send in a text message
									send_string = str(route_name) + " - " + str(route_time) + "\n"
									final_send += send_string
							elif int(split_time[0]) > hour:
								i += 1 #if the hour is the same or greater and the minutes are greater we have a valid next stop time
								route_name = time.trip.route.route_shortname
								route_time = time.arrival_time
								#construct our string we will send in a text message
								send_string = str(route_name) + " - " + str(route_time) + "\n"
								final_send += send_string
					#send our reply
					twilio_client.sms.messages.create(to=sender, from_="+12509842369", body=final_send)	
					return render_to_response("gtfs_bus/success.html", RequestContext(request))
				except:
					#send reply if error happens
					twilio_client.sms.messages.create(to=sender, from_="+12509842369", body="No Stop Found")	
					raise
					return render_to_response("gtfs_bus/default.html", RequestContext(request))
	


def display_route(request, pk, dow="Weekday"):
	direction = request.GET.get('dir', '')
	route = Route.objects.get(id=pk)
	calendars = Calendar.objects.all()
	our_calendars = []
	for calendar in calendars:
		if calendar.start_date < date.today() and calendar.end_date > date.today():
			our_calendars += Calendar.objects.filter(service_id = calendar.service_id)
	if direction:
		trips = Trip.objects.filter(route=route, day=dow, headsign = direction, service_id__in = our_calendars)
	else:
		trips = Trip.objects.filter(route=route, day=dow, service_id__in = our_calendars)
	busses = Bus.objects.filter(trip__in = trips)
	stops = Stops.objects.filter(~Q(light_num=0), stoptimes__trip__in = trips)
	stop_times = StopTimes.objects.filter(trip__in = trips, stop__in = stops).order_by('trip', 'stop_sequence')
	stop_times_stop = StopTimes.objects.filter(trip__in = trips, stop__in = stops, stop_sequence = 1).order_by('display_time')
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
			'center': maps.LatLng(48.4633,-123.311800),
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
	context = {'direction': direction, 'dow': dow, 'trips': trips, 'stops': stops, 'form': MapForm(initial={'map':gmap}), 'busroute':route, 'stop_times_stop': stop_times_stop, 'stop_times':stop_times}
	return render_to_response("gtfs_bus/route_detail.html", context, RequestContext(request))

	
#API Calls

#BusDetail 
#Description: gives us a list of busses for the route given
class BusDetail(generics.RetrieveAPIView):
	model = Bus
	serializer_class = BusSerializer
	def get(self, request, route, format=None):
		bus_list = []
		our_route = Route.objects.get(route_id = route)
		our_trips = Trip.objects.filter(route = our_route)
		for trips in our_trips:
			try:
				bus_list += Bus.objects.filter(trip = trips)
			except:
				pass
		serializer = BusSerializer(bus_list)
		return Response(serializer.data)
#ScheduleDetail
#Description: gives us a list of stop_times given a route and headsign
class ScheduleDetail(generics.RetrieveAPIView):
	model = StopTimes
	serializer_class = StopTimesSerializer
	def get(self, request, route, headsign, format=None):
		calendars = Calendar.objects.all()
		our_calendars = []
		for calendar in calendars:
			if calendar.start_date < date.today() and calendar.end_date > date.today():
				our_calendars += Calendar.objects.filter(service_id = calendar.service_id)
		our_route = Route.objects.get(route_id = route)
		our_trips = Trip.objects.filter(route=our_route, headsign=headsign, service_id__in = our_calendars)
		stop_times = StopTimes.objects.filter(trip__in = our_trips).order_by('trip', 'stop_sequence')
		serializer = StopTimesSerializer(stop_times)
		return Response(serializer.data)

#ArrivalsAtStop
#Description: gives stop times based on stop_id and day of week given
class ArrivalsAtStop(generics.RetrieveAPIView):
	model = StopTimes
	serializer_class = StopTimesSerializer
	def get(self, request, stop_id, dow, format=None):
		calendars = Calendar.objects.all()
		our_calendars = []
		for calendar in calendars:
			if calendar.start_date < date.today() and calendar.end_date > date.today():
				our_calendars += Calendar.objects.filter(service_id = calendar.service_id)
		our_trips = Trip.objects.filter(day=dow, service_id__in = our_calendars)
		our_stop = Stops.objects.get(stop_id = stop_id)
		stop_times = StopTimes.objects.filter(trip__in = our_trips, stop = our_stop).order_by('arrival_time')
		serializer = StopTimesSerializer(stop_times)
		return Response(serializer.data)

#RouteDetail
#Description: gives a list of routes
class RouteDetail(generics.RetrieveAPIView):
	model = Route
	serializer_class = RouteSerializer
	def get(self, request, format=None):
		our_routes = Route.objects.all()
		serializer = RouteSerializer(our_routes)
		return Response(serializer.data) 

class NextStopTime(generics.RetrieveAPIView):
	model = StopTimes
	serializer_class = StopTimesSerializer
	def get(self, request, trip_id, stop_id, format=None):
		calendars = Calendar.objects.all()
		our_calendars = []
		for calendar in calendars:
			if calendar.start_date < date.today() and calendar.end_date > date.today():
				our_calendars += Calendar.objects.filter(service_id = calendar.service_id)
		our_trip = Trip.objects.get(trip_id=trip_id, service_id__in = our_calendars)
		our_stop = Stops.objects.get(stop_id=stop_id)
		stop_times = StopTimes.objects.filter(trip = our_trip, stop=our_stop)
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
				if h_diff < h_curr and m_diff < m_curr:
					m_curr = m_diff
					h_curr = h_diff
					next_stop = stop
		serializer = StopTimesSerializer(next_stop)
		return Response(serializer.data)

#LightDetail
#Description: Gives a list of lights that should be lit up on our microcontroller
class LightDetail(generics.RetrieveAPIView):
	model = Stops
	serializer_class = SimpleStopsSerializer
	def get(self, request, route, format=None):
		calendars = Calendar.objects.all()
		our_calendars = []
		for calendar in calendars:
			if calendar.start_date < date.today() and calendar.end_date > date.today():
				our_calendars += Calendar.objects.filter(service_id = calendar.service_id)
		stops_final = []
		our_route = Route.objects.get(route_id = route)
		our_trips = Trip.objects.filter(route=our_route, service_id__in = our_calendars)
		our_bus = Bus.objects.filter(trip__in = our_trips)
		our_stops = Stops.objects.filter(~Q(light_num=0), stoptimes__trip__in = our_trips)
		stop_dict = {}
		bus_dict = {}
		for bus in our_bus:
			bus_dict[bus] = 10000
		for stop in our_stops:
			for bus in our_bus:
				distance = helpers.distance_on_unit_sphere(stop.lat, stop.lon, bus.lat, bus.lon)
				if bus_dict[bus] > distance:
					bus_dict[bus] = distance
					stop_dict[bus.id] = stop.id
		for key in stop_dict:
			stops_final += Stops.objects.filter(id = stop_dict[key])
		serializer = SimpleStopsSerializer(stops_final)
		return Response(serializer.data)
