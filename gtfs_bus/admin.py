from django.contrib import admin
from gtfs_bus.models import *


admin.site.register(Route, RouteAdmin)
admin.site.register(Calendar, CalendarAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(Bus, BusAdmin)
admin.site.register(Stops, StopsAdmin)
admin.site.register(StopTimes, StopTimesAdmin)
