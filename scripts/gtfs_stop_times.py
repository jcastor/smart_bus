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
		time_depart = row[2]
		time.arrival_time = time_arrive
		time.departure_time = time_depart
		time.stop_sequence = row[4]
		time_display = time_arrive.split(':')
		if int(time_display[0]) >= 24:
			time_display[0] = int(time_display[0]) - 24
			if time_display > 10:		
				time_display[0] = str(time_display[0])
				time_display = ":".join(time_display)
			else:
				number = str(time_display[0])
				time_display[0] = '0'
				time_display[0] + number
				time_display = ":".join(time_display)
		else:
			time_display = ":".join(time_display)
		time.display_time = time_display
		time.departure_time = time_depart
		time.save()
	except Exception as e:
		print e
		sys.exit("There was an error loading the stop_times.txt file \
				Please read the above error to troubleshoot")
print "Finished loading stop_times " + sys.argv[1]
