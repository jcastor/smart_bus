django_project_home="/home/jcastor/django/499project/smart_bus"
import sys,os
sys.path.append(django_project_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'smart_bus.settings'

from bus_tracker.models import BusRoute, BusStop, Direction, ArrivalTime, Bus, BusLocation, Light
import csv, re

data2 = open(sys.argv[1])

cr2 = csv.reader(data2)

#Loading Routes

#loading Stops


for row in cr2:
	route = BusRoute.objects.get(route_id="26-Victoria")
	stop = BusStop.objects.get(stop_name=row[0])
	try:
		arrivaltime = ArrivalTime.objects.get(route=route, stop=stop, time=row[1])
	except:
		arrivaltime = ArrivalTime()
		arrivaltime.route = route
		arrivaltime.stop = stop
		time = row[1]
		if row[1].startswith("24"):
			time = list(row[1])
			time[0] = '0'
			time[1] = '0'
			time = "".join(time)
		arrivaltime.time = time
		arrivaltime.save()

print "finished"
