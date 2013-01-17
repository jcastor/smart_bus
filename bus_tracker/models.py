from django.db import models
from django.contrib import admin

class BusRoute(models.Model):
	number = models.IntegerField()
	def __unicode__(self):
		return self.number

class BusStop(models.Model):
	phone_number = models.IntegerField()
	stop_name = models.CharField(max_length=100)
	routes = models.ManyToManyField('BusRoute')
	lon = models.DecimalField(max_digits=8, decimal_places=6)
	lat = models.DecimalField(max_digits=8, decimal_places=6)
	def __unicode__(self):
		return self.stop_name

class Bus(models.Model):
	phone_number = models.IntegerField()
	id_number = models.CharField(max_length=60)
	bus_route = models.ForeignKey('BusRoute')
	bus_stops = models.ManyToManyField('BusStop')
	def __unicode__(self):
		return self.id_number

class BusLocation(models.Model):
	bus = models.OneToOneField('Bus')
	lon = models.DecimalField(max_digits=8, decimal_places=6)
	lat = models.DecimalField(max_digits=8, decimal_places=6)	
	time = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		location = lon + " " + lat
		return self.location

class Light(models.Model):
	id_num = models.IntegerField()
	route = models.ForeignKey('BusRoute')
	lon = models.DecimalField(max_digits=8, decimal_places=6)
	lat = models.DecimalField(max_digits=8, decimal_places=6)
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
