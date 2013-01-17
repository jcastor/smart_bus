from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView, TemplateView

from django.views.generic.simple import direct_to_template

urlpatterns = patterns('bus_tracker.views',
	url(r'^$', TemplateView.as_view(template_name="bus_tracker/default.html"), name="main"),
	url(r'^sms/$', 'sms'),
)
