django_project_home="/home/jcastor/django/499project/smart_bus"
import sys,os
sys.path.append(django_project_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'smart_bus.settings'

from bus_tracker.models import BusRoute, BusStop, Direction, ArrivalTime, Bus, BusLocation, Light
import csv, re

data1 = open(sys.argv[1])
data2 = open(sys.argv[2])

cr = csv.reader(data1)
cr2 = csv.reader(data2)

eastpattern = r'^(eastbound)'
westpattern = r'^(westbound)'
northpattern = r'^(northbound)'
southpattern = r'^(southbound)'



eastregex = re.compile(eastpattern, re.IGNORECASE)
westregex = re.compile(westpattern, re.IGNORECASE)
northregex = re.compile(northpattern, re.IGNORECASE)
southregex = re.compile(southpattern, re.IGNORECASE)
#Loading Routes
for row in cr:
	newroute = BusRoute()
	newroute.route_id = row[0]
	newroute.route_short_name = row[1]
	newroute.save()

#loading Stops


east = Direction.objects.get(name="East")
west = Direction.objects.get(name="West")
north = Direction.objects.get(name="North")
south = Direction.objects.get(name="South")
nonedirection = Direction.objects.get(name="None")
for row in cr2:
	findEast = eastregex.match(row[1])
	findWest = westregex.match(row[1])
	findNorth = northregex.match(row[1])
	findSouth = southregex.match(row[1])
	route = BusRoute.objects.get(route_id=row[0])
	stop_name = row[1]
	try:
		newstop = BusStop.objects.get(stop_name=stop_name)
		newstop.routes.add(route)
		if findEast:
			newstop.direction = east
		elif findWest:
			newstop.direction = west
		elif findNorth:
			newstop.direction = north
		elif findSouth:
			newstop.direction = south
		else:
			newstop.direction = nonedirection
	except:
		newstop = BusStop()
		newstop.stop_name = stop_name
		newstop.phone_number = "+15551234567"
		newstop.lat=row[2]
		newstop.lon=row[3]
		if findEast:
			newstop.direction = east
		elif findWest:
			newstop.direction = west
		elif findNorth:
			newstop.direction = north
		elif findSouth:
			newstop.direction = south
		else:
			newstop.direction = nonedirection
		newstop.save()
		newstop.routes.add(route)
print "finished"
