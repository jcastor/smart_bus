from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView, DetailView, TemplateView
from django.views.decorators.cache import cache_page
from django.db.models import Q
from bus_tracker.models import BusRoute, BusLocation, Bus
from django import forms
from gmapi import maps
from gmapi.forms.widgets import GoogleMap


def sms(request):
	textmessage = request.GET.get('Body', '')
	sender = request.GET.get('From', '')
	if textmessage:
		splitmessage = textmessage.split(';')
		#messages should arrive in the form of lat;loni
		bus = Bus.objects.get(phone_number=sender)
		updatelocation = BusLocation.objects.get(bus=bus)
		updatelocation.lat = splitmessage[0]
		updatelocation.lon = splitmessage[1]
		updatelocation.save()

	return render_to_response("bus_tracker/default.html", RequestContext(request))

class MapForm(forms.Form):
	map = forms.Field(widget=GoogleMap(attrs={'width':510, 'height':510}))

def displayroute(request, pk):
	route = BusRoute.objects.get(id=pk)
	lat = route.bus_set.get().buslocation.lat
	lon = route.bus_set.get().buslocation.lon
	gmap = maps.Map(opts = {
		'center': maps.LatLng(lat, lon),
		'mapTypeId': maps.MapTypeId.ROADMAP,
		'zoom': 13,
		'mapTypeControlOptions': {
			'style': maps.MapTypeControlStyle.DROPDOWN_MENU
		},
	})
	for stop in route.busstop_set.all():
		marker = maps.Marker(opts = {
			'map': gmap,
			'position': maps.LatLng(stop.lat, stop.lon),
		})
	marker2 = maps.Marker(opts = {
		'map': gmap,
		'position': maps.LatLng(lat, lon),
	})
	maps.event.addListener(marker2, 'mouseover', 'myobj.markerOver')
	maps.event.addListener(marker2, 'mouseout', 'myobj.markerOut')
	info = maps.InfoWindow({
		'content': 'Current Bus Location',
		'disableAutoPan': True
	})
	info.open(gmap, marker2)	

	context = {'form': MapForm(initial={'map':gmap}), 'busroute': route}
	return render_to_response("bus_tracker/busroute_detail.html", context, RequestContext(request))
	
