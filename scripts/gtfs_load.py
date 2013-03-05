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
	try:
		trip = Trip.objects.get(trip_id = row[0])
		stop = Stops.objects.get(stop_id = row[3])
		time = StopTimes()
		time.trip = trip
		time.stop = stop
		time_arrive = row[1]
		time.stop_sequence = row[4]
		if time_arrive.startswith("24"):
			time_arrive = list(time_arrive)
			time_arrive[0] = '0'
			time_arrive[1] = '0'
			time_arrive = "".join(time_arrive)
		time.arrival_time = time_arrive
		time_depart = row[2]
		if time_depart.startswith("24"):
			time_depart = list(time_depart)
			time_depart[0] = '0'
			time_depart[1] = '0'
			time_depart = "".join(time_depart)
		time.departure_time = time_depart
		time.save()
		print time
	except Exception as e:
		print e

