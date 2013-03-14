from rest_framework import serializers
from gtfs_bus.models import *

class TripSerializer(serializers.ModelSerializer):
	class Meta:
		model = Trip
		fields = ('id', 'trip_id', 'day', 'headsign')
class BusSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bus
		depth = 2
		trip = TripSerializer()

class StopsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Stops

class SimpleStopsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Stops
		fields = ('stop_id', 'light_num')

class StopTimesSerializer(serializers.ModelSerializer):
	class Meta:
		model = StopTimes
		depth = 2
		trip = TripSerializer()
		stop = StopsSerializer()

class RouteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Route
