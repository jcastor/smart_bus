from django.db import models
from django.contrib import admin

class Route(models.Model):
	route_id = models.CharField(max_length=120)
	route_shortname = models.CharField(max_length=300)
	route_long_name = models.CharField(max_length=500)
	def __unicode__(self):
		return self.route_id

class Trip(models.Model):
	trip_id = models.IntegerField()
	route = models.ForeignKey('Route')
	day = models.CharField(max_length=30)
	headsign = models.CharField(max_length=150)
	def __unicode__(self):
		return unicode(self.trip_id)

class Bus(models.Model):
	trip = models.ForeignKey('Trip')
	phone_num = models.CharField(max_length=30)
	lat = models.DecimalField(max_digits=30, decimal_places=12)
	lon = models.DecimalField(max_digits=30, decimal_places=12)
	def __unicode__(self):
		return self.phone_num

class Stops(models.Model):
	stop_name = models.CharField(max_length=300)
	phone_num = models.CharField(max_length=30)
	stop_id = models.IntegerField()
	lat = models.DecimalField(max_digits=30, decimal_places=12)
	lon = models.DecimalField(max_digits=30, decimal_places=12)
	light_num = models.IntegerField(blank=True)
	def __unicode__(self):
		return self.stop_name

class StopTimes(models.Model):
	trip = models.ForeignKey('Trip')
	stop = models.ForeignKey('Stops')
	arrival_time = models.TimeField()
	departure_time = models.TimeField()
	stop_sequence = models.IntegerField()
	def __unicode__(self):
		return unicode(self.arrival_time)

class RouteAdmin(admin.ModelAdmin):
	search_fields = ["route_id"]
class TripAdmin(admin.ModelAdmin):
	search_fields = ["trip_id"]
class BusAdmin(admin.ModelAdmin):
	search_fields = ["phone-num"]
class StopsAdmin(admin.ModelAdmin):
	search_fields = ["stop_id"]
class StopTimesAdmin(admin.ModelAdmin):
	search_fields = ["arrival_time"]
