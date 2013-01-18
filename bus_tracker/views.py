from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView, DetailView, TemplateView
from django.views.decorators.cache import cache_page
from django.db.models import Q
from bus_tracker.models import BusRoute, BusLocation, Bus
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
