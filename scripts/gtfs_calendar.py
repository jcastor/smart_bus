django_project_home="/home/jcastor/django/499project/smart_bus"
import sys,os
sys.path.append(django_project_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'smart_bus.settings'
from datetime import date
from gtfs_bus.models import *
import csv, re

data2 = open(sys.argv[1])

cr2 = csv.reader(data2)


for row in cr2:
	calendar = Calendar()
	calendar.service_id = row[0]
	start_date = row[8]
	construct_date_start = date(int(start_date[:4]), int(start_date[4:6]), int(start_date[6:8]))
	calendar.start_date = construct_date_start
	end_date = row[9]
	construct_date_end = date(int(end_date[:4]), int(end_date[4:6]), int(end_date[6:8]))
	calendar.end_date = construct_date_end
	calendar.save()

print "Finished loading calendar"
