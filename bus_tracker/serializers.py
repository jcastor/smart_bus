from rest_framework import serializers
from bus_tracker.models import BusLocation

class BusLocationSerializer(serializers.ModelSerializer):
	class Meta:
		model = BusLocation
		fields = ('bus', 'lon', 'lat')
