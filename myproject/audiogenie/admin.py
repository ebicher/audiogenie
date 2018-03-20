from django.contrib import admin

# Register your models here.

from .models import Project, Track, Log

class TrackInLine(admin.StackedInline):
    model = Track
    extra = 1

class LogInLine(admin.StackedInline):
    model = Log
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['project_name']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        ('Song key', {'fields': ['song_key']}),
        ('Notes', {'fields': ['project_notes']}),
        ('Users', {'fields': ['users']}),
        ('Main Users', {'fields': ['main_user']}),
        ('Image', {'fields': ['project_img']})
        
    ]
    inlines = [TrackInLine]

admin.site.register(Project, ProjectAdmin)