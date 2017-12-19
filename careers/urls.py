from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.all_careers, name='all_careers'),
	url(r'^(?P<category_slug>[-\w]+)/$', views.all_careers, name='all_careers_by_category'),
	url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.career_detail, name='career_detail'),   
]
