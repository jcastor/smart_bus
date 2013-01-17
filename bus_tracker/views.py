from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView, DetailView, TemplateView
from django.views.decorators.cache import cache_page
from django.db.models import Q
from bus_tracker.models import BusRoute
def sms(request):
	textmessage = request.GET.get('Body', '')
	if textmessage:
		b1 = BusRoute(number=1)
		b1.save()

	return render_to_response("bus_tracker/default.html", RequestContext(request))
