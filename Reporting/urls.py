from django.conf.urls import include, url
from django.conf import settings
import Reporting.views as views
import django.contrib.auth.views as auth_views
from rest_framework import routers





urlpatterns = [
    url(r'^Sana_Plus/(?P<username>[\w.@+-]+)/(?P<token_apps>[^\s\.,!?]{32})/(?P<code_Events>[^\s\.,!?]{6})/events.js/$',views.check_Reporting_link,name='Check_Report'),
    url(r'^Sana_Plus/(?P<username>[\w.@+-]+)/(?P<token_apps>[^\s\.,!?]{32})/(?P<code_Events>[^\s\.,!?]{6})/realtime.js/$',views.realtime_Reporting_link, name='realtime_report'),
    url(r'^reloads/$',views.reloads, name='Events'),
    url(r'^Page_ranking/$', views.page_ranking_record, name='Page_Ranking'),
    url(r'^Reservations_Record/$', views.Reservetion_Record, name='Reservation_Record'),
    url(r'^Seller_Record/$', views.Seller_Record, name='Seller_Record'),
    url(r'^Visited_Product/$', views.Visited_Product_Record, name='Visited_Product'),
    url(r'^Search_Product/$', views.Search_Product_Record, name='Search_Product'),
    url(r'^Register_user/$', views.Register_user_record, name='register_user'),

]