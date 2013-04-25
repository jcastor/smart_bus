# File: serializer.py
# Description: Model serializers for django-rest framework
# serializers with Simple prefix are for api's that are called
# by embedded devices that may not have enough memory for
# complete model

from rest_framework import serializers
from gtfs_bus.models import *


class RouteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Route

class SimpleRouteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Route
		fields = ('route_shortname',)

class TripSerializer(serializers.ModelSerializer):
	route = RouteSerializer()
	class Meta:
		model = Trip
		exclude = ('id',)
		fields = ('route','trip_id', 'day', 'headsign')

class SimpleTripSerializer(serializers.ModelSerializer):
	route = SimpleRouteSerializer()
	class Meta:
		model = Trip
		exclude = ('id',)
		fields = ('route',)

class BusSerializer(serializers.ModelSerializer):
	trip = TripSerializer()
	class Meta:
		model = Bus
		depth = 2

class StopsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Stops
		exclude = ('id',)

class SimpleStopsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Stops
		fields = ('stop_id', 'light_num')

class StopTimesSerializer(serializers.ModelSerializer):
	trip = TripSerializer()
	stop = StopsSerializer()
	class Meta:
		model = StopTimes

class SimpleStopTimesSerializer(serializers.ModelSerializer):
	trip = SimpleTripSerializer()
	class Meta:
		depth = 2
		model = StopTimes
		fields = ('display_time', 'trip')
