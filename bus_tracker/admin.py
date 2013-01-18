from django.contrib import admin
from bus_tracker.models import ArrivalTime, ArrivalTimeAdmin, BusRoute, BusRouteAdmin, BusStop, BusStopAdmin, Bus, BusAdmin, BusLocation, BusLocationAdmin, Light, LightAdmin

admin.site.register(BusRoute, BusRouteAdmin)
admin.site.register(BusStop, BusStopAdmin)
admin.site.register(Bus, BusAdmin)
admin.site.register(BusLocation, BusLocationAdmin)
admin.site.register(Light, LightAdmin)
admin.site.register(ArrivalTime, ArrivalTimeAdmin)
