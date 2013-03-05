from rest_framework import serializers
from gtfs_bus.models import *

class BusSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bus
		fields = ('trip', 'phone_num', 'lat', 'lon')

class StopTimesSerializer(serializers.ModelSerializer):
	class Meta:
		model = StopTimes
		fields = ('trip','stop','departure_time')

class TripSerializer(serializers.ModelSerializer):
	class Meta:
		model = Trip
		fields = ('id', 'trip_id', 'day', 'headsign')
