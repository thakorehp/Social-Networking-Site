from django.conf.urls import url,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from friendship.models import FriendshipRequest

app_name = 'marvel'

urlpatterns = [
    url(r'^$', views.login_user, name='index'),
    url(r'^forgot/$', views.forgot, name='forgot'),
    url(r'^register/$', views.register, name='register'),
    url(r'^change/$', views.change_password, name='change'),    
        # url(r'^Home/$', views.login_user, name='login_user'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^timeline/$', views.timeline, name='timeline'),
    url(r'^Notifications/$', views.notifications, name='notifications'),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name='change_friends'),
    url(r'^fprofile/(?P<user>.+)/',views.other_profile,name='friprofile'),
    # url(r'^logout_user/$', views.logout_user, name='logout_user'),
    # url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^fr_profile/(?P<frid>[0-9])/$', views.frprofile, name='frprofile'),
    url(r'^tril/$', views.tril, name='tril'),
    # url(r'^schedule_post/$', views.schedule, name='schedule'),
    url(r'^chat/$', views.chat, name='chat'),
    # url(r'^Welcome/$', views.new, name='new'),
    url(r'^friends/$', views.friends, name='friends'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]