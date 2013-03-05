django_project_home="/home/jcastor/django/499project/smart_bus"
import sys,os
sys.path.append(django_project_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'smart_bus.settings'

from gtfs_bus.models import *
import csv, re

data2 = open(sys.argv[1])

cr2 = csv.reader(data2)

#Loading Routes

#loading Stops


for row in cr2:
	route = Route.objects.get(route_id="26-Victoria")
	route_id = row[0]
	try:
		if route_id == "26-Victoria":
			new_trip = row[2]
			trip = Trip()
			trip.trip_id = new_trip
			trip.route = route
			day = row[1].split('-')
			day2 = day[2]
			trip.day = day2
			trip.headsign = row[4]
			trip.save()
	except exception as e:
		print e
