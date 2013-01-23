from django.db import models
from django.contrib import admin

class BusRoute(models.Model):
	route_id = models.CharField(max_length=200)
	route_short_name = models.CharField(max_length=200)
	def __unicode__(self):
		return unicode(self.route_short_name)

class Direction(models.Model):
	name = models.CharField(max_length=30)
	def __unicode__(self):
		return self.name


class BusStop(models.Model):
	phone_number = models.CharField(max_length=30)
	stop_name = models.CharField(max_length=100, unique=True)
	routes = models.ManyToManyField('BusRoute')
	lon = models.DecimalField(max_digits=20, decimal_places=6)
	lat = models.DecimalField(max_digits=20, decimal_places=6)
	direction = models.ForeignKey('Direction')
	def __unicode__(self):
		return self.stop_name


class ArrivalTime(models.Model):
	route = models.ForeignKey('BusRoute')
	stop = models.ForeignKey('BusStop')
	time = models.TimeField()
	def __unicode__(self):
		return unicode("Route: " + str(self.route.route_short_name) + " stop: " + str(self.stop.stop_name) + " time: " + str(self.time))

class Bus(models.Model):
	phone_number = models.CharField(max_length=30)
	id_number = models.CharField(max_length=60)
	bus_route = models.ForeignKey('BusRoute')
	bus_stops = models.ManyToManyField('BusStop')
	def __unicode__(self):
		return self.id_number

class BusLocation(models.Model):
	bus = models.OneToOneField('Bus')
	lon = models.DecimalField(max_digits=20, decimal_places=6)
	lat = models.DecimalField(max_digits=20, decimal_places=6)
	time = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.bus.phone_number

class Light(models.Model):
	id_num = models.IntegerField()
	route = models.ForeignKey('BusRoute')
	lon = models.DecimalField(max_digits=20, decimal_places=6)
	lat = models.DecimalField(max_digits=20, decimal_places=6)
	def __unicode__(self):
		return self.id_num


class BusRouteAdmin(admin.ModelAdmin):
	search_fields = ["number"]
class BusStopAdmin(admin.ModelAdmin):
	search_fields = ["stop_name"]

class BusAdmin(admin.ModelAdmin):
	search_fields = ["id_number"]

class BusLocationAdmin(admin.ModelAdmin):
	search_fields = ["bus"]

class LightAdmin(admin.ModelAdmin):	
	search_fields = ["id_num"]

class ArrivalTimeAdmin(admin.ModelAdmin):
	search_fields = ["route"]

class DirectionAdmin(admin.ModelAdmin):
	search_fields = ["name"]
