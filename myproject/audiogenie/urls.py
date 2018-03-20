from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from audiogenie import views as core_views


urlpatterns = [
    url(r'^$', core_views.index, name='index'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),    
    url(r'^about/$', core_views.about, name='about'),
    url(r'^contact/$', core_views.contact, name='coontact'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^project_create/$', core_views.project_create, name='project_create'),
    url(r'^(?P<project_id>[0-9]+)/$', core_views.detail, name='detail'),
    url(r'^(?P<project_id>[0-9]+)/add_note/$', core_views.add_note, name='add_note'),
    url(r'^(?P<project_id>[0-9]+)/track_create/$', core_views.track_create, name='track_create'),
    url(r'^(?P<track_id>[0-9]+)/delete_tra/$', core_views.delete_track, name='delete_track'),
    url(r'^(?P<project_id>[0-9]+)/delete_pro/$', core_views.delete_pro, name='delete_pro'),
    url(r'^(?P<project_id>[0-9]+)/add_friend/$', core_views.add_friend, name='add_friend'),
    url(r'^(?P<project_id>[0-9]+)/del_friend/$', core_views.del_friend, name='del_friend'),
]
