from django.conf.urls import url
from django.contrib import admin
from web import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^projects[/]+$', views.projects, name='projects'),
    url(r'^project/(?P<id>\d+)[/]+$', views.project, name='project'),
    url(r'^project/(?P<id>\d+)/[^/]+[/]+$', views.project, name='project'),
    url(r'^resume[/]+$', views.generic, name='resume'),
    url(r'^social[/]+$', views.social, name='social'),
    url(r'^faq[/]+$', views.faq, name='faq'),
    url(r'^blog[/]+$', views.generic, name='blog'),
    url(r'^tags[/]+$', views.tags, name='tags'),
    url(r'^socialtags[/]+$', views.socialtags, name='socialtags'),
    url(r'^calendar[/]+$', views.generic, name='calendar'),
    url(r'^admin/', admin.site.urls),
]
