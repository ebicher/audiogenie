from django import forms
from django.contrib.auth.models import User
from audiogenie.models import Project, Track
from django.forms import ModelForm

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        
class ProjectForm(ModelForm):
	project_name = forms.CharField(max_length=100, required=True)
	song_key = forms.CharField(max_length=10, required=False)
	project_notes =  forms.CharField(max_length=500, required=False)
	project_img =  forms.FileField(required=False)
	
	class Meta:
	    model = Project
	    fields = ['project_name', 'song_key', 'project_notes']
	    
class TrackForm(forms.Form):
	track_name = forms.CharField(max_length=30, required=True)
	instrument = forms.CharField(max_length=30, required=False)
	track_notes =  forms.CharField(max_length=500, required=False)
	tempo =  forms.DecimalField(required=False)
	track_file =  forms.FileField(required=True)
	
	class Meta:
	    model = Track
	    fields = ['track_name', 'instrument', 'track_notes', 'tempo', 'track_file']