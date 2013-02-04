from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView, TemplateView
from bus_tracker.models import BusRoute
from django.views.generic.simple import direct_to_template
from bus_tracker import views

urlpatterns = patterns('bus_tracker.views',
	url(r'^$', TemplateView.as_view(template_name="bus_tracker/default.html"), name="main"),
	url(r'^sms/$', 'sms'),
	url(r'^routes/', ListView.as_view(model=BusRoute, context_object_name="busroute_list",), name="busroute_list"),
	url(r'^route/(?P<pk>\d+)/$', 'displayroute', name="displayroute"),
	url(r'^route/(?P<pk>\d+)/(?P<direction>\w+)/$', 'displayroute', name="displayroute_direction"),
	url(r'^rest/(?P<bus>\w+)/$', views.BusLocationDetail.as_view()),

)
