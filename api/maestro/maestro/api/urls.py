from django.conf.urls import patterns, url

urlpatterns = patterns('maestro.api.views',
    url(r'^$', 'root'),
    url(r'^users/$', 'create_user'),
    url(r'^sessions/$', 'login'),
    url(r'^stories/$', 'new_story'),
)
