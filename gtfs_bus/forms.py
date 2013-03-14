from gmapi.forms.widgets import GoogleMap
from django import forms


#Map form is our form field for the google map display
class MapForm(forms.Form):
	map = forms.Field(widget=GoogleMap(attrs={'width':510, 'height':510}))
