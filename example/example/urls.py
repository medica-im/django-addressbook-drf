from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'example.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
# Django-addressbook url patterns
urlpatterns += patterns('',
    # .
    url(r'^addressbook/', include('addressbook.urls')),
    # .
)
