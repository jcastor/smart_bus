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
#format is route_id, route_shortname, route_longname

for row in cr2:
	route = Route()
	route.route_id = row[0]
	route.route_shortname = row[1]
	route.route_long_name = row[2].strip('"')
	route.save()

print "Finished loading routes"
