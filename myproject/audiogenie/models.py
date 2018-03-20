# Model page
# Created by Evan Bicher
# Date - 10/13/15
# Updated - 2/20/18

import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# from sorl.thumbnail import ImageField

# Class for the song which is linked to a user (and superuser) and multiple tracks
class Project(models.Model):
	project_name = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date project created')
	song_key = models.CharField(max_length=100, null=True)
	project_notes = models.CharField(max_length=600, null=True)
	users = models.ManyToManyField(User)  					#Allows users to have many projects and vice versa
	project_img = models.ImageField(upload_to = 'media/project_images/', default='/static/audiogenie/img/project.jpg')
	main_user = models.CharField(max_length=30, null=True)
	def __str__(self):
		return self.project_name
	
# Class for music tracks for each project
class Track(models.Model):
	creation_user = models.ForeignKey(User, on_delete=models.CASCADE)					
	project = models.ForeignKey('Project', on_delete=models.CASCADE)
	track_name = models.CharField(max_length=200)
	instrument = models.CharField(max_length=200, null=True)
	tempo = models.DecimalField(max_digits=6, decimal_places=2, null=True)
	track_date = models.DateTimeField('track added date')
	track_notes = models.CharField(max_length=600, null=True)
	track_file = models.FileField(upload_to = 'media/tracks/', null=True)
	def __str__(self):
		return self.track_name
		
		
# Class for an edit log that says changes and notes
class Log(models.Model):
	project = models.ForeignKey('Project', on_delete=models.CASCADE)
	edit_time = models.DateTimeField('time edited')
	note = models.CharField(max_length=600)
	def __str__(self):
		return self.note
	