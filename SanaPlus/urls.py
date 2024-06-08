from django.conf.urls import include, url
from django.conf import settings
import SanaPlus.views as views
import django.contrib.auth.views as auth_views
import Reporting.views as Reporting_views


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^add_admin/$', views.Create_admin_site, name="add_admin"),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.dj_logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name="log_out"),

    url(r'^password_change/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.password_change,name="password_change"),
    url(r'^password_change_done/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.change_password_done, name="password_change_done"),
# Manage User
    url(r'^add_user/$', views.Create_User, name='add_user'),
#Manage Apps
    url(r'^Manage_apps/$', views.Create_Apps, name='Create_Apps'),
    url(r'^Delete_apps/(?P<app_id>\d+)/$',views.delete_apps, name='Delete_apps'),
#Manage Events
    url(r'^ManageEvents/(?P<id_apps>\d+)/$',views.Manage_Events, name='ManageEvents'),
    url(r'^ManageEventsURLs/(?P<apps_id>\d+)/(?P<Events_id>\d+)/$',views.Create_URlS, name='CreateUrls'),
    url(r'^Sana_Plus/(?P<username>[\w.@+-]+)/(?P<token_apps>[^\s\.,!?]{32})/(?P<code_Events>[^\s\.,!?]{6})/(?P<date_request>\d{4}[-]\d{2}[-]\d{2}\s\d{2}[:]\d{2}[:]\d{2})/$',views.records_Urls,name='happening_events'),
    url(r'^DeleteEvents/(?P<apps_id>\d+)/(?P<code_Events>[^\s\.,!?]{6})/$',views.delete_Events, name='DeleteEvents'),
    # Reporting Part
    url(r'^Render_Report/(?P<username>[\w.@+-]+)/(?P<apps_code>[^\s\.,!?]{32})/(?P<code_Events>[^\s\.,!?]{6})/$' ,views.render_report, name='Render_Report'),
    url(r'^form_Report/(?P<username>[\w.@+-]+)/(?P<apps_code>[^\s\.,!?]{32})/(?P<code_Events>[^\s\.,!?]{6})/$',views.report, name='form_Report'),
    url(r'^form_Report/(?P<username>[\w.@+-]+)/(?P<apps_code>[^\s\.,!?]{32})/(?P<code_Events>[^\s\.,!?]{6})/(?P<str_tag_events>[\[\s\'\w{6}\'\:\'\w{1,}\'\s\,\'\w{1,}\'\:\'\w{1,}\'\]]{1,})/$',views.charts_detaile, name='details'),


]


#Sana_Plus/admin_21/RsBwEgdAhSXWfqaaaauuuIkXONs8TsVC/4cwZ4o/2018-09-26 10:25:34.6080o00

# \[\s\'\w{6}\'\:\'\w{1,}\'\s\,\'\w{1,}\'\:\'\w{1,}\'\]{1,}    for [ 'idName':'addddd' ,'TagName':'1111']