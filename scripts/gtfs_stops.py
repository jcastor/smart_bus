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
	stop = Stops()
	stop.stop_name = row[1]
	stop.phone_num = "+"
	stop.stop_id = row[0]
	stop.lat = row[3]
	stop.lon = row[4]
	stop.light_num = 0
	stop.save()
print "Finished loading stops"
