from rest_framework import serializers
from gtfs_bus.models import *

class RouteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Route

class TripSerializer(serializers.ModelSerializer):
	route = RouteSerializer()
	class Meta:
		model = Trip
		exclude = ('id',)
		fields = ('trip_id', 'day', 'headsign')

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

