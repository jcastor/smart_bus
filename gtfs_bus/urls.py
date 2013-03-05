from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView, TemplateView
from gtfs_bus.models import Route
from django.views.generic.simple import direct_to_template
from gtfs_bus import views

urlpatterns = patterns('gtfs_bus.views',
	url(r'^$', TemplateView.as_view(template_name="gtfs_bus/default.html"), name="main"),
	url(r'^routes/', ListView.as_view(model=Route, context_object_name="route_list",), name="route_list"),
)