from rest_framework import serializers
from bus_tracker.models import BusLocation, BusStop, Light

class BusLocationSerializer(serializers.ModelSerializer):
	class Meta:
		model = BusLocation
		fields = ('bus', 'lon', 'lat')


class BusStopSerializer(serializers.ModelSerializer):
	class Meta:
		model = BusStop
		fields = ('phone_number', 'stop_name', 'routes', 'lat', 'lon', 'direction')


class LightSerializer(serializers.ModelSerializer):
	class Meta:
		model = Light
		fields = ('id_num', 'route', 'stop')
