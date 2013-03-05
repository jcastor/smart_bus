from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView, DetailView, TemplateView
from django.views.decorators.cache import cache_page
from django.db.models import Q
from gtfs_bus.models import *
from django import forms
from gmapi import maps
from gmapi.forms.widgets import GoogleMap
from django_twilio.client import twilio_client
from rest_framework import generics
from rest_framework.response import Response
import math

class MapForm(forms.Form):
	map = forms.Field(widget=GoogleMap(attrs={'width':510, 'height':510}))

def displayroute(request, pk):
	route = Route.objects.get(id=pk) 
