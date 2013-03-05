  1 from django.shortcuts import render_to_response
  2 from django.template import RequestContext
  3 from django.views.generic import ListView, DetailView, TemplateView
  4 from django.views.decorators.cache import cache_page
  5 from django.db.models import Q
  6 from gtfs_bus.models import *
  7 from django import forms
  8 from gmapi import maps
  9 from gmapi.forms.widgets import GoogleMap
 10 from django_twilio.client import twilio_client
 12 from rest_framework import generics
 13 from rest_framework.response import Response
 14 import math

class MapForm(forms.Form):
	map = forms.Field(widget=GoogleMap(attrs={'width':510, 'height':510}))

def displayroute(request, pk):
	route = Route.objects.get(id=pk) 
