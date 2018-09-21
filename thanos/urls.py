
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import login
from marvel.views import re_no,view_not,Add_Room,AROOM,ser_user,view_post

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^marvel/', include('marvel.urls', namespace='marvel')),
    url(r'^', include('marvel.urls')),
    url(r'^accounts/login/', include('marvel.urls')),
    url(r'^removenot/',re_no),
    url(r'^getnot/',view_not),
    url(r'^chat_f/',Add_Room),
    url(r'^test2/$',AROOM),
    url(r'^getpost/',view_post),
    url(r'^ajax/validate_username/',ser_user),
]
if settings.DEBUG:	
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)