from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView, TemplateView
from gtfs_bus.models import Route
from django.views.generic.simple import direct_to_template
from gtfs_bus import views

urlpatterns = patterns('gtfs_bus.views',
	url(r'^$', TemplateView.as_view(template_name="gtfs_bus/default.html"), name="main"),
	url(r'^update/$', 'update_location'),
	url(r'^routes/(?P<pk>\w+)/(?P<dow>\w+)/$', 'display_route', name="display_route"),
	url(r'^routes/(?P<pk>\w+)/$', 'display_route', name="display_route"),
	url(r'^routes/', ListView.as_view(model=Route, context_object_name="route_list",), name="route_list"),
	url(r'^rest/buslocations/(?P<route>\w+)/$', views.BusDetail.as_view()),
	url(r'^rest/next_arrival_at_stop/(?P<trip_id>\w+)/(?P<stop_id>\w+)/$', views.NextStopTime.as_view()),
	url(r'^rest/schedule/(?P<route>\w+)/$', views.ScheduleDetail.as_view()),
	url(r'^rest/lights/(?P<route>\w+)/$', views.LightDetail.as_view()),
)
