from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.template import loader
from .models import Project, Track, Log
from django.shortcuts import render, render_to_response, get_object_or_404


from django.utils import timezone
from .forms import UserForm, ProjectForm, TrackForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User


#This view is the home page where you see the possible songs
@login_required(login_url='/audiogenie/login/')
def index(request):
	project_list = Project.objects.filter(users = request.user)
	template = loader.get_template('index.html')
	context = {
		'project_list': project_list,
	}
	return render(request, 'index.html', context)

#This view sends the project selected from the index screen
@login_required(login_url='/audiogenie/login/')
def detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    main_user = project.main_user
    log_set = Log.objects.filter(project=project).order_by('-edit_time')
    return render(request, 'detail.html', {'project': project,'log_set': log_set}  )

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

	
#This view creates a project 
@login_required(login_url='/audiogenie/login/')
def project_create(request):
	if request.method == 'POST':
		form = ProjectForm(request.POST, request.FILES)
		if form.is_valid():
			project_name = request.POST['project_name']
			song_key = request.POST['song_key']
			project_notes = request.POST['project_notes']
			pub_date = pub_date=timezone.now()
			users=request.user
			#this if statement is just to find out if they uploaded an image
			if 'project_img' in request.FILES:
				project_img = request.FILES['project_img']
				newProject = Project(project_name=project_name, song_key=song_key, project_notes=project_notes, pub_date=pub_date, project_img=project_img)
			else:
				newProject = Project(project_name=project_name, song_key=song_key, project_notes=project_notes, pub_date=pub_date)
			newProject.main_user=users.username
			newProject.save()
			newProject.users.add(users) # connects current user to the project
			newProject.save()
#			add_log = Log(edit_time=timezone.now(), note= 'The user: '+ str(users) + 'created the project "' str(project_name) '" ')
#			add_log.project = newProject
			add2_log = Log(edit_time=timezone.now(), note= 'Creation Notes: ' + str(project_notes))
			add2_log.project = newProject
			add2_log.save()
			return HttpResponseRedirect('/audiogenie/'+str(newProject.id)+'/')
		else:
			return HttpResponse("You must enter a project name!")
	else:
		return render(request, 'project_create.html')

		
#This view creates a music tracks for the projects
@login_required
def track_create(request, project_id):
	project = get_object_or_404(Project, pk=project_id)
	if request.method == 'POST':
		tform = TrackForm(request.POST, request.FILES)
		if tform.is_valid():
			track_name = request.POST['track_name']
			tempo = request.POST['tempo']
			instrument = request.POST['instrument']
			track_notes = request.POST['track_notes']
			track_date = pub_date=timezone.now()
			track_file = request.FILES['track_file']
			newTrack = Track(track_name=track_name, tempo=tempo, instrument=instrument, track_notes=track_notes, creation_user=request.user, track_date=track_date, track_file=track_file)
			newTrack.project = project #connects the track to the project
			newTrack.save()
			mainuser=request.user
			cre_log = Log(edit_time=timezone.now(), note=str(mainuser.username)+ ' added the track: '+str(track_name)+' to the project.')
			cre_log.project = project
			cre_log.save()
			cre2_log = Log(edit_time=timezone.now(), note=str(track_name)+'\'s track notes: '+str(track_notes))
			cre2_log.project = project
			cre2_log.save()
			return HttpResponseRedirect('/audiogenie/'+str(project.id)+'/')
		else:
			return HttpResponse("Needs a name and file!")
	else:
		return render(request, 'track_create.html', {'project': project})

#this view deletes the track, i don't think that it deletes the files from the server so that could be an issue on a larger scale!		
def delete_track(request, track_id):
	track = get_object_or_404(Track, pk=track_id)
	project = track.project
	mainuser = request.user
	del_log = Log(edit_time=timezone.now(), note=str(mainuser.username)+ ' deleted the track: '+str(track.track_name)+' from the project.')
	del_log.project = project
	del_log.save()
	track.delete()
	return HttpResponseRedirect('/audiogenie/'+str(project.id)+'/')
	
#This deletes a project and returns the user to the home/index page/view
def delete_pro(request, project_id):
	project = get_object_or_404(Project, pk=project_id)
	project.delete()
	return HttpResponseRedirect('/audiogenie/')		
	
	
	
#this view is called when someone wants to add a note on a project, it just updates the db and brings the user back to the project screen	
def add_note(request, project_id):
	thatuser=request.user
	project = get_object_or_404(Project, pk=project_id)
	if request.method == 'POST':
		add_note = request.POST['add_note']
		add_log = Log(edit_time=timezone.now(), note= str(thatuser.username)+' says: ' + str(add_note))
		add_log.project = project
		add_log.save()
		return HttpResponseRedirect('/audiogenie/'+str(project.id)+'/')
	else:
		return HttpResponse("Error, please click back and try again.")


def add_friend(request, project_id):
	project = get_object_or_404(Project, pk=project_id)
	if request.method == 'POST':
		user = request.POST['user']
		theuser = User.objects.filter(username = user)
		if theuser.exists():
			theuser = User.objects.get(username = user)
			project.users.add(theuser)
			project.save()
			mainuser=request.user
			add_log = Log(edit_time=timezone.now(), note= str(mainuser.username)+ ' added the user: '+str(theuser.username)+' to the project.')
			add_log.project = project
			add_log.save()
			return HttpResponseRedirect('/audiogenie/'+str(project.id)+'/')
		else:
			return HttpResponse("That's not their username, hit back and try again!!!!")

def del_friend(request, project_id):
	project = get_object_or_404(Project, pk=project_id)
	if request.method == 'POST':
		user = request.POST['user']
		theuser = User.objects.filter(username = user)
		if theuser.exists():
			theuser = User.objects.get(username = user)
			project.users.remove(theuser)
			project.save()
			mainuser=request.user
			del_log = Log(edit_time=timezone.now(), note= str(mainuser.username)+ ' removed the user: '+str(theuser.username)+' from the project.')
			del_log.project = project
			del_log.save()
			return HttpResponseRedirect('/audiogenie/'+str(project.id)+'/')
		else:
			return HttpResponse("Name not valid!")


		

		

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})