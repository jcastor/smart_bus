from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView, TemplateView
from gtfs_bus.models import Route
from django.views.generic.simple import direct_to_template
from gtfs_bus import views

urlpatterns = patterns('gtfs_bus.views',
	url(r'^$', ListView.as_view(model=Route, context_object_name="route_list",), name="home_route_list"),
	url(r'^update/$', 'process_sms'),
	url(r'^routes/(?P<pk>\w+)/(?P<dow>\w+)/$', 'display_route', name="display_route_dow"),
	url(r'^routes/(?P<pk>\w+)/$', 'display_route', name="display_route"),
	url(r'^routes/', ListView.as_view(model=Route, context_object_name="route_list",), name="route_list"),
	url(r'^rest/buslocations/(?P<route>[-\w]+)/$', views.BusDetail.as_view()),
	url(r'^rest/routes/$', views.RouteDetail.as_view()),
	url(r'^rest/upcoming_stop_times/(?P<stop_id>\w+)/(?P<num_times>\w+)/$', views.UpcomingStopTimes.as_view()),
	url(r'^rest/next_arrival_at_stop/(?P<trip_id>\w+)/(?P<stop_id>\w+)/$', views.NextStopTime.as_view()),
	url(r'^rest/arrivals_at_stop/(?P<stop_id>\w+)/(?P<dow>\w+)/$', views.ArrivalsAtStop.as_view()),
	url(r'^rest/schedule/(?P<route>[-\w]+)/(?P<headsign>\w+)/$', views.ScheduleDetail.as_view()),
	url(r'^rest/lights/(?P<route>[-\w]+)/$', views.LightDetail.as_view()),
)
