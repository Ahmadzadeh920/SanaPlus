# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
import django.contrib.auth as auth
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.views.decorators.http import require_POST
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.models import User,Permission,Group
from django.http import request

from django.contrib.auth import logout as django_logout
from django.http import HttpResponseRedirect
from rest_framework import status
from .utils import grecaptcha_verify

from django.contrib.auth import logout as django_logout
from django.contrib.auth import authenticate
from .forms import Change_password ,Forms_Create_Urls
from django.contrib.auth.decorators import login_required
from .models import relation_parent_user, Apps_tokens_admin , type_apps , Events_Apps ,Happening_Events
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.crypto import get_random_string
from django.contrib.auth.middleware import get_user
from django.contrib.auth import login as auth_login
import sys, urllib
import time
from Reporting.models import (
                    Record_Events,
                    PageRank,
                    Reserve,
                    Sell,
                    visited_Product,
                    Search_Product,
                    Register_user,
                    )


from django.http import HttpResponse
from .fusioncharts import FusionCharts
import datetime as date
from collections import OrderedDict
import ast
import numpy as np
import json
import re
@csrf_exempt

#----------------------Global Variable





# Create your views here.
# return index.html

def index(request):
    return render(request,'index.html')




#--------------------------------ADD uSER
from django.core.exceptions import PermissionDenied



# this function is called others function with params is_staff and is_superUser is passed.
def _add_user(request,is_staff,is_superuser):

    if is_superuser or is_staff: # check User is admin or Super User
        if request.method=='POST': # check form is send via Post method
            if request.POST.has_key('requestcode'):  # check the requset code
                if request.user.is_authenticated(): # check user is authenticated
                    if request.POST['username'] and request.POST['password'] and request.POST['email'] and request.POST['password_confirm']: # check all fields is full
                        if request.POST['password']==request.POST['password_confirm']:
                            email=request.POST['email']
                            username=request.POST['username']
                            if not User.objects.filter(email=email).exists(): # check the email is exists
                                if not User.objects.filter(username=username).exists(): # check the username is exists

                                    password= make_password(request.POST['password'])
                                    now = datetime.now()
                                    if is_superuser and is_staff: # identity is super User and can add admin
                                        this_user = User.objects.create(email=email , username=username ,
                                                                        is_staff=True , is_superuser=False , last_login=now ,
                                                                        date_joined=now , password=password)
                                        this_goups = Group.objects.get(name='Admin_Site')
                                        this_user.groups.add(this_goups)
                                        if this_user and this_goups:
                                            message = 'ثبت نام ادمین با موفیت انجام شد'
                                            context = {
                                                'message': message}
                                            return render(request , 'index.html' , context)
                                        else:
                                            message = 'مجدد تلاش کنید'
                                            context = {
                                                'message': message}
                                            return render(request , 'index.html' , context)

                                    elif not is_superuser and is_staff: # identity Admin saite and Can added User
                                        this_user = User.objects.create(email=email , username=username ,
                                                                        is_staff=False , is_superuser=False ,
                                                                        last_login=now ,
                                                                        date_joined=now , password=password)
                                        this_goups = Group.objects.get(name='User_Site')
                                        this_user.groups.add(this_goups)
                                        user_admin = User.objects.get(email=request.user.email)
                                        rel_admin_child = relation_parent_user.objects.create(parent=user_admin.id ,
                                                                                              child=this_user)
                                        if this_user and this_goups and rel_admin_child:
                                            message = 'ثبت نام کاربر با موفیت انجام شد'
                                            context = {
                                                'message': message}
                                            return render(request , 'index.html' , context)
                                        else:
                                            message = 'مجدد تلاش کنید'
                                            context = {
                                                'message': message}
                                            return render(request , 'index.html' , context)
                                    else:
                                        context = {
                                            'message':'ssssssss'}
                                        return render(request, 'add_user.html', context)

                                else:
                                    massage = {'massage': 'این نام کاربری ثبت شده است '}
                            else:
                                massage = {'massage': 'این ایمیل ثبت شده است  '}

                        else:
                            massage = {'massage': 'پسوردها با یکدیگر تطابق ندارد'}
                    else:
                        massage = {'massage': 'تمامی فیلدها باید پر شود'}
                else:
                    massage = {'massage': 'شما باید  لاگین شوید'}
                    return render(request , 'login.html' , context=massage)
            else:
                massage = {'massage':'این کد فعال سازی معتبر نیست. در صورت نیاز دوباره تلاش کنید'}

        elif request.method=='GET' and is_superuser:
            massage={'massage':'اضافه کردن ادمین سایت'}
            return render(request, 'add_user.html', context=massage)
        else:
            massage = {'massage': 'اضافه کردن کاربر '}
            return render(request,'add_user.html',context=massage)
    else:
       raise PermissionDenied




# Create Admin Sait
def Create_admin_site(request):
    if request.user.is_superuser:
        return _add_user(request, True, True)
    else:
        return render(request, 'index.html', context={'massage': 'شما سطح دسترسی ندارید'})


# Create User
def Create_User(request):
   if request.user.groups.filter(name__in=['Admin_Site']).exists(): # identity request user is belonge to Admin_Site
        admin_groups = Group.objects.get(name='Admin_Site')
        set_admin_permission= admin_groups.permissions.all()
        check_per=set_admin_permission.get(codename='add_user')
        if check_per:
            return _add_user(request , True , False)
        else:
            massage = {'massage': 'شما اجازه دسترسی ندارید '}
            return render(request, 'index.html', context=massage)

   else:
       raise PermissionDenied





















#------------------------------------------ Render Login

@csrf_exempt
# Login function

def login(request):
    if not request.user.is_authenticated(): #  check the user is authenticated
    # check if POST objects has username and password

        if request.method=='POST': # checks the methods
            if not grecaptcha_verify(request):  # captcha was not correct
                context = {
                    'message': 'کپچای گوگل درست وارد نشده بود. شاید ربات هستید؟'}  # TODO: forgot password
                return render(request, 'login.html', context)
            else:

                if request.POST.has_key('requestcode'): # checks the spam or not
                    if request.POST.has_key('username') and request.POST.has_key('password'):
                        username = request.POST['username']
                        password = request.POST['password']
                        this_user=authenticate(username=username, password=password)
                        if (this_user):  # authentication
                            now = datetime.now()
                            this_user.last_login=now
                            this_user.save()
                            auth_login(request, this_user)
                            context = {
                                'user': this_user}  # TODO: forgot password
                            # TODO: keep the form data
                            return render(request, 'index.html', context)

                        else:
                            context = {
                                'message': 'نام کاربری و رمز عبور اشتباه می باشد'}  # TODO: forgot password
                            # TODO: keep the form data
                            return render(request, 'login.html', context)
                    else:
                        context = {
                            'message': 'نام کاربری و رمز عبور وارد کنید'}  # TODO: forgot password
                        # TODO: keep the form data
                        return render(request, 'login.html', context)
                else:
                    context = {
                        'message': 'کد معتبر نمی باشد . '}
                    return render(request, 'login.html', context)

        else:
            context = {
                    'message': 'به صفحه لاگین خوش آمدید'}
            return render(request, 'login.html', context)
    else:
        context={'massage':'شما به عنوان یکی از کاربران شناخته شده اید میتواننیداز خروج استفاده کنید'}
        return render(request, 'index.html', context)


def dj_logout(request,next_page):
    django_logout(request)
    return render(request,'index.html',{'massage_logout':' به درستی خارج شده اید می توانید از صفحه لاگین وارد شوید'})

#---------------------------------------Change_password

# password change
# input email which user is authenticate
#output return forms of change passwords
def password_change(request,email):
    user=User.objects.get(email=email)
    if user:
        form= Change_password()
        return render(request , 'password_change_form.html' ,{'form': form,'user':user })
    else:
        form= login_From()
        return render(request,'login.html',{
        'form':form,
        'context':'به صفحه ورود خوش آمدید',

})



#----------------------Change_password_done:
# password change done and changed is saved in database
# input email which user is authenticate
#output save updates passwords in db
def change_password_done(request,email):
    if request.method=='POST':
        user=User.objects.get(email=email)
        pass_old=user.check_password(request.POST['old_pass'])
        if pass_old and request.POST['new_pass']==request.POST['confirm_new_pass']:

            user.save_base(force_update=True,update_fields=user.set_password(request.POST['new_pass']))
            return render(request , 'password_change_done.html' ,{'user': user,
                                                                  'change_password_done':True})
        else:
            return render(request , 'password_change_done.html' ,{'change_password_done':False,
                                                               'user': user})

    else:
        form = Change_password
        return render(request , 'password_change_form.html' ,
                      {'form': form , })



#----------------------------Token
@csrf_exempt
# Create Application and if user authenticated has applications, list all of the applications
#returns page Manage Applications
def Create_Apps(request):
    if request.user.is_authenticated()and request.user.is_staff:
        if request.method=='POST':
            if request.POST.has_key('requestcode'):  #
                name_apps=request.POST['name_apps']
                date_create=datetime.now()
                type_apps_select=request.POST['type_apps']
                token=get_random_string(length=32)

                if type_apps.objects.filter(name=type_apps_select).exists():
                    get_type_apps = type_apps.objects.get(name=type_apps_select)
                    if name_apps:
                        Create_apps_admin = Apps_tokens_admin.objects.create(name=name_apps,
                                                                             date_create_apps=date_create,
                                                                             user_token=request.user,
                                                                             type_apps=get_type_apps, token=token, )

                        if Apps_tokens_admin.objects.filter(user_token=request.user).exists():
                            call_apps_objects = Apps_tokens_admin.objects.filter(user_token=request.user)
                            return render(request, 'Manage_apps.html', {
                                'apps_object': call_apps_objects,
                                 'massage': 'به درستی وارد شد',
                            })
                        else:
                            return render(request, 'Manage_apps.html', {
                                'apps_object': None,
                                'massage': 'به درستی وارد شد',
                            })



                        return render(request, 'Manage_apps.html', {
                               })

                    else:

                        return render(request, 'Manage_apps.html', {
                            'massage': 'نام اپلیکیشن باید وارد نمایید'})

                else:

                    return render(request, 'Manage_apps.html', {
                        'massage': 'نوع اپلیکشن معتبر نمی باشد'})
            else:
                return render(request, 'Manage_apps.html', {
                    'massage': 'این کد فعال سازی معتبر نمی باشد'})

        else:
            if Apps_tokens_admin.objects.filter(user_token=request.user).exists():
                call_apps_objects=Apps_tokens_admin.objects.filter(user_token=request.user)
                return render(request,'Manage_apps.html', {
                    'apps_object': call_apps_objects})

            else:
                return render(request, 'Manage_apps.html', {
                    'apps_object': None})

    else:
        return render(request, 'index.html', {
            'massage': 'شما باید از ادمین سایت باشید و در خواست توکن دهید و سطح دسترسی به این بخش را ندارید'})


#----------------------------------------------------- Delete_Apps:

# Remove application which is selected and save changes in db
# inputs:  id_apps which is selected

def delete_apps(request,app_id):
    if request.user.is_authenticated:
        if Apps_tokens_admin.objects.filter(id=app_id).exists():
            obj_App=Apps_tokens_admin.objects.get(id=app_id)
            if Events_Apps.objects.filter(apps_events=obj_App).exists():
                Events_Apps.objects.filter(apps_events=obj_App).delete()
                if Happening_Events.objects.filter(apps=obj_App).exists():
                    Happening_Events.objects.filter(apps=obj_App).delete()
            del_apps=Apps_tokens_admin.objects.filter(id=app_id).delete()
            return redirect(Create_Apps)

        else:
            return render(request,'index.html',{'massage':'انتخاب اپلیکشن مجدد انجام شود'})
    else:
        return render(request,'login.html',{'massage':'شما باید از لاگین شوید'})




#-------------------------------------------Create Events for every apps

# Creare Events and list of events that is belong to apps which selected
# input id of apps thst is selected
def Manage_Events(request , id_apps):
    if request.user.is_authenticated() and request.user.is_staff:
        obj_apps = Apps_tokens_admin.objects.get(id=id_apps)
        if request.method=='POST':
            if request.POST.has_key('requestcode'):  #
                name_Events=request.POST['name_Events']
                date_create=datetime.now()
                descript_Events=request.POST['descrip_Events']
                code_Events=get_random_string(length=6)
                if Apps_tokens_admin.objects.filter(id=id_apps).exists():
                    obj_token= Apps_tokens_admin.objects.get(id=id_apps)
                    if obj_token:
                        if name_Events and descript_Events:

                            Create_Event = Events_Apps.objects.create(name=name_Events,date_create_Events=date_create,  apps_events_id=obj_token.id, code=code_Events, descrip=descript_Events)


                            if Events_Apps.objects.filter(apps_events_id=obj_token).exists():
                                call_Events_objects = Events_Apps.objects.filter(apps_events_id=obj_token)
                                return render(request, 'Manage_Events.html', {
                                    'Event_object':call_Events_objects,
                                     'massage': 'به درستی وارد شد',
                                    'obj_apps': obj_apps

                                })
                            else:
                                return render(request, 'Manage_Events.html', {
                                    'Event_object': None,
                                    'massage': 'به درستی وارد شد',

                                    'obj_apps':obj_apps
                                })





                        else:

                            return render(request, 'Manage_Events.html', {
                                'massage': 'نام و شرح  events باید وارد نمایید',

                                'obj_apps': obj_apps,


                            })
                    else:
                        return render(request, 'Manage_apps.html', {
                            'massage': 'اپلیکشن انتخاب شده نا معتبر است',

                            'obj_apps': obj_apps,


                        })
                elif id_apps == 0:

                    return render(request, 'Manage_apps.html', {
                        'massage': 'افزودن Events ',

                        'obj_apps': obj_apps,


                    })

                else:

                    return render(request, 'Manage_apps.html', {
                        'massage': 'اپلیکشن انتخاب شده نامعتبر است',

                        'obj_apps': obj_apps,


                    })
            else:
                return render(request, 'Manage_apps.html', {
                    'massage': 'این کد فعال سازی معتبر نمی باشد',
                    'id_apps':id_apps,
                    'obj_apps': obj_apps,

                })

        else:
            obj_token = Apps_tokens_admin.objects.filter(id=id_apps)
            if Events_Apps.objects.filter(apps_events_id=obj_token).exists():
                call_Events_objects = Events_Apps.objects.filter(apps_events_id=obj_token)
                return render(request, 'Manage_Events.html', {
                    'Event_object': call_Events_objects,
                    'obj_apps': obj_apps,

                })
            else:
                return render(request, 'Manage_Events.html', {
                    'Event_object': None,
                    'obj_apps': obj_apps,

                })

    else:
        return render(request, 'index.html', {
            'massage': 'شما باید از ادمین های سایت باشید و در خواست توکن دهید و سطح دسترسی به این بخش را ندارید'})

#____________________________________________________________Create URls
#Create Urls which requested urls for every events
#input id of selected apps and id of selected events
#output string which is passed must be included username\apps_token\Event_tokn
def Create_URlS(request, apps_id, Events_id):
    if request.user.is_authenticated:
        if apps_id and Events_id:
            if Apps_tokens_admin.objects.filter(id=apps_id).exists():
                obj_apps=Apps_tokens_admin.objects.get(id=apps_id)
                if Events_Apps.objects.filter(id=Events_id).exists():
                    obj_Events=Events_Apps.objects.get(id=Events_id)
                    if obj_Events.apps_events_id==obj_apps.id:
                        user_name=request.user.username
                        now=datetime.now()
                        str_now=now.strftime('%Y-%m-%d %H:%M:%S')
                        urls_input='Sana_Plus/'+user_name+'/'+str(obj_apps.token)+'/'+str(obj_Events.code)+'/'
                        call_Events_objects = Events_Apps.objects.filter(apps_events_id=obj_apps)

                        return render(request, 'Manage_Events.html', {'massage': '',
                                                                      'Event_object': call_Events_objects,
                                                                      'apps_id': apps_id,
                                                                      'urls_input': urls_input,
                                                                      'forms_Create_Urls':Forms_Create_Urls,
                                                                      'obj_apps':obj_apps
                                                                      })
                    else:
                        call_Events_objects = Events_Apps.objects.filter(apps_events_id=obj_apps)
                        return render(request, 'Manage_Events.html', {'massage': 'Events انتخاب شده مربوط به این اپلیکشن نمی باشد ',
                                                                      'Event_object': call_Events_objects,
                                                                      'apps_id': apps_id,
                                                                      'obj_apps':obj_apps,
                                                                      })


                else:
                    call_Events_objects = Events_Apps.objects.filter(apps_events_id=obj_apps)
                    return render(request, 'Manage_Events.html', {'massage': ' Events انتخاب شده نامعتبر است ',
                                                                'Event_object': call_Events_objects,
                                                                'apps_id': apps_id,
                                                                  'obj_apps':obj_apps
                                                                })

            else:
                return render(request,'Manage_apps.html',{'massage':'اپلیکیشن انتخاب شده معتبر است '})

        else:
            return render(request,'Manage_apps.html', {'massage': 'اپلیکشن و Events انتخاب شده نامعتبر است'})



    else:
        return render(request,'login.html',
                      {'massage':'شما باید از ادمین های سایت باشید'}
                      )

#-----------------------------------------------
# if user visit requested urls , this happen is inserted on Happening_Events
# input : username of authenticated user,token of apps , token of Events , date of requested urls
# output: inserts in Happening_Events
def records_Urls(request,username,token_apps,code_Events,date_request):
    if request.user.is_authenticated and username:
        if request.user.username==username and Apps_tokens_admin.objects.filter(token=token_apps).exists() and Events_Apps.objects.filter(code=code_Events).exists():
            obj_app=Apps_tokens_admin.objects.get(token=token_apps)
            if obj_app.user_token==request.user:
                obj_Events=Events_Apps.objects.get(code=code_Events)
                if obj_Events.apps_events==obj_app:
                    try:
                        check_date = time.strptime(date_request,'%Y-%m-%d %H:%M:%S')
                        if not Happening_Events.objects.filter(user=request.user,apps=obj_app,Events=obj_Events,date=date_request).exists():
                            obj_happens=Happening_Events.objects.create(user=request.user,apps=obj_app,Events=obj_Events,date=date_request)
                            return HttpResponse('create do ')
                        else:
                           return HttpResponse('exits ')
                    except ValueError:
                        return HttpResponse('not ok')
                else:
                    return render(request, 'Manage_Events.html', {'massage': 'این Events مربوط به این اپلیکشن نمی باشد '})


            else:
                return render(request, 'Manage_Events.html', {'massage': 'شما دسترسی به این Events ندارید'})

        else:
            return render(request, 'Manage_Events.html', {'massage': 'مجدد درخواست URLS برای Events مربوطه دهید'})

    else:
        return render(request,'login.html', {'massage':'شما باید لاگین شوید'})

###########-----------------------------------------------delete Events
# Delete Events which selected
# input : id of apps selected and id of selected Events
# output: Delete selected Events and save in db

def delete_Events(request,apps_id,code_Events):
    if request.user.is_authenticated:
        if  Apps_tokens_admin.objects.filter(id=apps_id).exists() and Events_Apps.objects.filter(code=code_Events).exists():
            obj_app=Apps_tokens_admin.objects.get(id=apps_id)
            obj_Events=Events_Apps.objects.get(code=code_Events)
            if obj_Events.apps_events==obj_app:
                if Happening_Events.objects.filter(Events=obj_Events).exists():
                    Happening_Events.objects.filter(Events=obj_Events).delete()

                obj_del=Events_Apps.objects.filter(code=code_Events).delete()
                if obj_del:
                    return redirect('ManageEvents',id_apps=apps_id)

                else:

                    return render(request, 'Manage_apps.html',
                                      {'massage': 'مجدد سعی شود'})


            else:
                return render(request, 'Manage_apps.html',
                                  {'massage': 'مجدداپلیکشن مربوطه را چک شود'})


        else:
            return render(request, 'Manage_apps.html', {'massage': 'شما دسترسی به این اپلیکشن ندارید یا Events مربوطه نامعتبر است  '})

    else:
        return render(request, 'login.html', {'massage': 'شما باید لاگین شوید'})


#____________________________________ Render Report
#Check user has this apps and this apps has this Events
#input : username of authenticated user , token of apps, token of events
# output: boolean check and massage

def checks_user_apps_events (request, username, apps_code, code_Events):
    if request.user.is_authenticated and request.user.username == username:
        if Apps_tokens_admin.objects.filter(user_token=request.user, token=apps_code).exists():
            obj_apps = Apps_tokens_admin.objects.get(token=apps_code)
            if Events_Apps.objects.filter(apps_events=obj_apps, code=code_Events).exists():
                obj_events = Events_Apps.objects.get(code=code_Events)
                return True, 'report_single.html' , 'به صفحه گزارش گیری خوش آمدید' ,obj_apps , obj_events
            else:
                return False, 'Manage_Events.html', 'you are not access to Events Or events code is mistake', obj_apps,None
        else:
            return False, 'Manage_apps.html', 'you are not access to application', None, None
    else:
        return False, 'login.html', 'you are must be one of the admin', None, None


# render page of report if checks_user_apps_events is true
# input : username of authenticated user , token of apps, token of events

def render_report(request,username,apps_code,code_Events):
    check , page, massage, obj_apps, obj_events= checks_user_apps_events (request, username, apps_code, code_Events)
    if check:
        return render(request,page,{'massage':massage,
                                    'obj_apps':obj_apps,
                                    'obj_events':obj_events
                                        })
    else:
        return render(request,page,{'massage':massage,
                                    'obj_apps':obj_apps,
                                        })




# checks start_time and end_time fir reporting and calculate the number of intervals based selected intervals
# input start_time,end_time,interval which user requested

def check_interval_time(start_time,end_time,interval):
    date_format = "%Y-%m-%d"
    start_time=datetime.strptime(start_time, date_format)
    end_time=datetime.strptime(end_time, date_format)
    interval=interval
    margin=end_time-start_time
    if interval=='day':
        count_inteval=margin.days
    elif interval=='week':
        count_inteval=abs(margin.days)/7
    elif interval=='month':
        count_inteval=abs(margin.days)/30
    else:
        count_inteval = 0
    return start_time,end_time,interval,margin,count_inteval

#if selected Events has data this selected intervals returns objects of this otherwise returns None
# input: code of selected events , Neme of models which wants to be reported , selected start_time, end_time,interval in reporting , and coun_intervals returned by check_interval_time
def check_report(event_code,Name_model,start_time, end_time,interval,count_inteval): # parameter Events_code and Name_Table
    obj_events=Events_Apps.objects.get(code=event_code)
    if Name_model.objects.filter(Event_id=obj_events.id ,date_record__range= (start_time,end_time)).exists():
        get_obj = Name_model.objects.filter(Event_id=obj_events.id ,date_record__range= (start_time,end_time)).all()
        return get_obj
    else:
        return  None

#_____________________________________
# that is returns charts for showing details of Javascript when cells of heatmap charts is linked
#input username of user , token of selected apps , token of selected Events , and obj of selected link
def charts_detaile(request,username,apps_code,code_Events,str_tag_events):
    #isinstance(some_object, basestring) checks type var is string
    match=re.findall("{u*\'\w{6,8}\'\:\su\'\w*\'\,\su*\'\w{1,8}\'\:\su\'\w*'}",str_tag_events)
    match_time=re.findall("{u*\'\w{6,8}\'\:\su\'\w*\'\,\su*\'\w{1,8}\'\:\su\'\w*\'\,\su\'\w{3,5}\'\:\s\d{1,}}",str_tag_events)
    list_id=[]

    array_match=[]
    if match:
        match_pattern=match
    elif match_time:
        match_pattern=match_time
    else:
        match_pattern=None

    if match_pattern:
        count_tag = [0 for x in range(len(match_pattern))]
        for i in range(0,len(match_pattern)):
           pattern_id_name=re.findall("\su\'\w{1,}\'\,",match_pattern[i])
           if pattern_id_name[0] in list_id:
               index=list_id.index(pattern_id_name[0])
               count_tag[index]+= 1
           else:
               list_id.append(pattern_id_name[0])
               count_tag[i] += 1
        dataSource = OrderedDict()

       # The `chartConfig` dict contains key-value pairs data for chart attribute
        chartConfig = OrderedDict()
        chartConfig["caption"] = 'تعداد رویدادها در رویداد جاوااسکریپت مورد نظر'
        chartConfig["subCaption"] = "تعداد رویداد مورد نظر در بازه های زمانی انتخاب شده "
        chartConfig["xAxisName"] = "ID_Elements "
        chartConfig["yAxisName"] = "تعداد"
        chartConfig["numberSuffix"] = "تعداد "
        chartConfig["yAxisMinValue"] = '1'
        chartConfig["yAxisMaxValue"] = '1000'
        chartConfig["plottooltext"] = "<b>$dataValue</b> apps were available on <b>$seriesName</b> in $label",
        chartConfig["theme"] = "Ocean"

       # The `chartData` dict contains key-value pairs data
        dataSource["chart"] = chartConfig
        dataSource["data"] = []
        for i in range(0,len(list_id)):
           data = {}
           data["label"] = list_id[i]
           data["value"] = count_tag[i]
           dataSource["data"].append(data)
        column2D = FusionCharts("column2d", "id_detailes_chart", "700", "300", "id_detailes_charts_container", "json",
                               dataSource)  # FusionCharts("column2d", "myFirstChart", "600", "400", "myFirstchart-container", "json", dataSource)
        return render(request,'report_single.html',{'id_detailes_chart':column2D.render()})

    else:
        return HttpResponse(str_tag_events)



#_______________________________________________ Chart Reports

# draw bar chats of on object which pass ,and  caption_charts, lable_column , yaxisname_str which passed
# input : object which must be reported , selected start_time, end_time , interval, count_interval which passed via check_interval_time, id_charts returned and id_charts_container is id of elements which included charts.  caption_charts, lable_column , yaxisname_str in charts must be strings
# output: return chrats
def chart(request,obj ,start_time, end_time , interval,count_inteval ,id_charts,id_charts_container,caption_charts, lable_column , yaxisname_str):
    count=[]
    chartData = OrderedDict()
    if count_inteval>0:
        for i in range(count_inteval):
            if interval=='week':
                end_time_interval=start_time+ date.timedelta(weeks=1)
            elif interval=='month':
                end_time_interval = start_time + date.timedelta(days=30)
            else:
                end_time_interval = start_time + date.timedelta(days=1)
            obj_interval=obj.filter(date_record__range= (start_time,end_time_interval)).all()
            count.append(len(obj_interval))
            chartData[i] = len(obj_interval)
            start_time=end_time_interval
        dataSource = OrderedDict()

        # The `chartConfig` dict contains key-value pairs data for chart attribute
        chartConfig = OrderedDict()
        chartConfig["caption"] = caption_charts
        chartConfig["subCaption"] = "تعداد  در بازه های زمانی انتخاب شده "
        chartConfig["xAxisName"] = "بازه زمانی "
        chartConfig["yAxisName"] = lable_column
        chartConfig["numberSuffix"] = "تعداد "
        chartConfig["yAxisMinValue"]='1'
        chartConfig["yAxisMaxValue"] = '1000'
        chartConfig["plottooltext"]= "<b>$dataValue</b> apps were available on <b>$seriesName</b> in $label",
        chartConfig["theme"] = "Ocean"

        # The `chartData` dict contains key-value pairs data
        dataSource["chart"] = chartConfig
        dataSource["data"] = []
        for key, value in chartData.items():
            data = {}
            data["label"] = key
            data["value"] = value
            dataSource["data"].append(data)
        column2D = FusionCharts("column2d", id_charts, "700", "300", id_charts_container, "json", dataSource) # FusionCharts("column2d", "myFirstChart", "600", "400", "myFirstchart-container", "json", dataSource)
        return column2D.render()
    else:
        return 'تعداد بازه های زمانی باید بیش از یک بازه زمانی باشد.'

#-------------------------------------Heat Map
# draw heatmap of on javascript events ,and  caption_charts, lable_column , yaxisname_str which passed
# input : javascript object which must be reported , selected start_time, end_time , interval, count_interval which passed via check_interval_time, id_charts returned and id_charts_container is id of elements which included charts.  caption_charts, lable_column , yaxisname_str in charts must be strings
# output: return heatmap chrats
def charts_heatmap(request,obj ,start_time, end_time , interval,count_inteval ,id_charts,id_charts_container,caption_charts, lable_column , yaxisname_str):
    Events_js= ["clicks", "dbclicks", "blur" , "submit" ,"mousemove" ,"onkeyup" ,"video" , "audio" , "drag_drop","img_load"]
    count=[[0 for x in Events_js ]for y in range(count_inteval)] # 6 is counts of events in js  0:clicks 1:dbclicks 2:blur 3:submit 4:mousemove 5:onkeyup
    details_str=[['' for x in Events_js ]for y in range(count_inteval)] # 6 is counts of events in js  0:clicks 1:dbclicks 2:blur 3:submit 4:mousemove 5:onkeyup
    dataSource = OrderedDict()
    if count_inteval>0 :
        for j in range(count_inteval):
            if interval == 'week':
                end_time_interval = start_time + date.timedelta(weeks=1)
            elif interval == 'month':
                end_time_interval = start_time + date.timedelta(days=30)
            else:
                end_time_interval = start_time + date.timedelta(days=1)
            obj_interval = obj.filter(date_record__range=(start_time, end_time_interval)).all()
            start_time=end_time_interval
            for i in range(len(obj_interval)):
                json_fields = obj_interval[i].json_fields
                clicks = json_fields['clicks']
                dbclicks = json_fields['dbclicks']
                blur = json_fields['blur']
                submit = json_fields['submit']
                mousemove = json_fields['mousemove']
                onkeyup = json_fields['onkeyup']
                video = json_fields['video']
                audio = json_fields['audio']
                drag_drop=json_fields['drag_drop']
                img_load = json_fields['img_load']
                count[j][0] += len(clicks)
                count[j][1] += len(dbclicks)
                count[j][2] += len(blur)
                count[j][3] += len(submit)
                count[j][4] += len(mousemove)
                count[j][5] += len(onkeyup)
                count[j][6] += len(video)
                count[j][7] += len(audio)
                count[j][8] += len(drag_drop)
                count[j][9] += len(img_load)
                if len(clicks)>0:
                    details_str[j][0] = str(clicks) + str(details_str[j][0])
                if len(dbclicks)>0:
                    details_str[j][1] = str(dbclicks) + str(details_str[j][1])
                if len(blur)>0:
                    details_str[j][2] = str(blur) + str(details_str[j][2])
                if len(submit)>0:
                    details_str[j][3] = str(submit) + str(details_str[j][3])
                if len(mousemove)>0:
                    details_str[j][4] = str(mousemove) + str(details_str[j][4])
                if len(onkeyup)>0:
                    details_str[j][5] = str(onkeyup) + str(details_str[j][5])
                if len(video)>0:
                    details_str[j][6] = str(video) + str(details_str[j][6])
                if len(audio)>0:
                    details_str[j][7] = str(audio) + str(details_str[j][7])
                if len(drag_drop)>0:
                    details_str[j][8] = str(drag_drop) + str(details_str[j][8])
                if len(img_load)>0:
                    details_str[j][9] = str(img_load) + str(details_str[j][9])

        data_list = []
        for i in range(0, len(count)):
            for j in range(0, len(count[i])):
                data_ = {}
                data_["rowid"] = str(i)
                data_["columnid"] = str(j)
                data_["value"] =count[i][j]
                data_["link"]=str(details_str[i][j])

                data_list.append(data_)
        column = []
        for k in range(0, len(Events_js)):
            data_col = {}
            data_col["id"] = k
            data_col["label"] = Events_js[k]
            column.append(data_col)
        row = []
        for h in range(0, count_inteval):
            data_rows = {}
            data_rows["id"] = str(h)
            data_rows["label"] = str(interval)+"_"+str(h+1)
            row.append(data_rows)
        # coustruct 2d array
        dataSource["columns"] = {}
        dataSource["columns"]["column"] = column
        dataSource["rows"] = {}
        dataSource["rows"]["row"] = row
        dataSource["dataset"] = {}
        dataSource["dataset"]["data"] = data_list


        chartObj = FusionCharts(
            'heatmap',
            id_charts,
            '600',
            '400',
            id_charts_container,
            'json',
            {
     "colorrange": {
       "gradient": "1",
       "minvalue": "0",
       "startlabel": "Poor",
       "endlabel": "Outstanding",

     },
     "dataset": [
       dataSource["dataset"]
     ],
     "columns": {
       "column": [
         {
           "id": "0",
           "label": "Clicks"
         },
         {
           "id": "1",
           "label": "dbclicks"
         },
         {
           "id": "2",
           "label": "blur"
         },
         {
           "id": "3",
           "label": "submit"
         },
         {
           "id": "4",
           "label": "mouse move"
         },
        {
               "id": "5",
               "label": "Key"
        },
           {
               "id": "6",
               "label": "Video"
           },
           {
               "id": "7",
               "label": "audio"
           },
           {
               "id": "8",
               "label": "drag_drop"
           },
           {
               "id": "9",
               "label": "image_ load"
           },

       ]
     },
     "rows": dataSource["rows"],
     "chart": {
       "theme": "fusion",
       "caption": caption_charts,
       "subcaption": "تعداد رویدادها در بازه های زمانی متفاوت",
       "xaxisname": lable_column,
       "yaxisname":yaxisname_str,
       "showvalues": "1",
       "valuefontcolor": "#ffffff",
       "plottooltext": "$rowlabel's $columnlabel grading score: <b>$value</b>"
     }
   })

        return chartObj.render()

    else:
        return 'تعداد بازه های زمانی باید بیش از یک بازه زمانی باشد.'





































# ----------------------------------------------------------------------
# checks all reporter must be showed and render page singe.reporter.html
# this function is called when forms od reporting is submitted
# input: username of authenticated user , token of selected apps and Events


def report(request,username,apps_code,code_Events):
    check, page, massage, obj_apps, obj_events = checks_user_apps_events(request, username, apps_code, code_Events)
    if check:
        if request.POST.has_key('requestcode'):
            start_time=request.POST.get('start_time')
            end_time=request.POST.get('end_time')
            intervals=request.POST.get('interval')
            if start_time and end_time and intervals and end_time>start_time:
                start_time, end_time, interval, margin, count_inteval=check_interval_time(start_time,end_time,intervals)
                if 0<count_inteval<10:
                    obj_reserve=check_report(code_Events,Reserve,start_time, end_time,interval,count_inteval)
                    obj_sell= check_report(code_Events,Sell,start_time, end_time,interval,count_inteval)
                    obj_Search_Product= check_report(code_Events,Search_Product,start_time, end_time,interval,count_inteval)
                    obj_visited_Product= check_report(code_Events,visited_Product,start_time, end_time,interval,count_inteval)
                    obj_Register_User= check_report(code_Events,Register_user,start_time, end_time,interval,count_inteval)
                    obj_Events_js= check_report(code_Events,Record_Events,start_time, end_time,interval,count_inteval)
                    if obj_reserve:
                        charts_reserve=chart(request,obj_reserve,start_time,end_time,interval,count_inteval,'charts_reserve','charts_reserve_container' ,
                                                                            'گزارش گیری رزرو', 'تعداد رزرو در بازه زمانی متفاوت ', 'تعداد')
                        #
                    else:
                        charts_reserve=None
                    if obj_sell:
                        charts_sell = chart(request, obj_sell, start_time, end_time, interval, count_inteval,
                                               'charts_sell', 'charts_sell_container', 'گزارش گیری فروش ',
                                               'تعداد فروش  در بازه زمانی متفاوت ', 'تعداد')
                    else:
                        charts_sell=None
                    if obj_Search_Product:
                        charts_search_Product = chart(request, obj_Search_Product, start_time, end_time, interval, count_inteval,
                                               'charts_search_Product', 'charts_Search_Product_container', 'گزارش گیری جستجوی محصولات ',
                                               'تعداد جستجو محصولات  در بازه زمانی متفاوت ', 'تعداد')
                    else:
                        charts_search_Product=None
                    if obj_visited_Product:
                        charts_visited_Product = chart(request, obj_visited_Product, start_time, end_time, interval,
                                                      count_inteval,
                                                      'charts_visited_Product', 'charts_visted_product_container',
                                                      'گزارش گیری جستجوی محصولات ',
                                                      'تعداد جستجو محصولات  در بازه زمانی متفاوت ', 'تعداد')
                    else:
                        charts_visited_Product=None

                    if obj_Register_User:
                        charts_Register_User = chart(request, obj_Register_User, start_time, end_time, interval,
                                                       count_inteval,
                                                       'charts_Register_User', 'charts_Register_User_container',
                                                       'گزارش گیری کاربران  ',
                                                       'تعداد جستجو کاربران  در بازه زمانی متفاوت ', 'تعداد')
                    else:
                        charts_Register_User =None


                    if obj_Events_js:
                        charts_Events_js =charts_heatmap(request, obj_Events_js, start_time, end_time, interval,
                                 count_inteval,
                                 'charts_Events_js', 'charts_Events_js_container',
                                 'گزارش گیری جاوا اسکریپت  ',
                                 'تعداد رویدادهای جاوا اسکریپتی   در بازه زمانی متفاوت ', 'بازه زمانی')

                    else:
                        charts_Events_js = None
                    if obj_reserve and obj_sell:
                        reserve_id=obj_reserve.values('Reservation_id')
                        sell_id=obj_sell.values('Reservation_id')
                        obj_reserve_sell=obj_sell
                        for i in range(0,len(reserve_id)):
                            if reserve_id[i] not in sell_id:
                                obj_reserve_sell.filter(Reservation_id=reserve_id[i]).delete()
                            else:
                                continue
                        charts_sell_reserve_both=chart(request, obj_reserve_sell, start_time, end_time, interval,
                                                       count_inteval,
                                                       'charts_sell_reserve_both', 'charts_sell_reserve_both_container',
                                                       'گزارش گیری تعداد فروش و رزرو با هم   ',
                                                       'تعداد فروش و رزرو با هم  در بازه زمانی متفاوت ', 'تعداد')

                    else:
                        charts_sell_reserve_both=None

                    return render(request, 'report_single.html', {'massage': 'نموادارهای گزارش گیری',
                                                                  'obj_apps': obj_apps,
                                                                  'obj_events': obj_events,
                                                                  'report':True,
                                                                  'charts_reserve':charts_reserve,
                                                                  'charts_sell':charts_sell,
                                                                  'charts_search_Product':charts_search_Product,
                                                                  'charts_visited_Product':charts_visited_Product,
                                                                  'charts_Register_User':charts_Register_User,
                                                                  'charts_Events_js':charts_Events_js,
                                                                  'charts_sell_reserve_both':charts_sell_reserve_both,
                                                                  })

                else:
                    return render (request,'report_single.html',{'massage':count_inteval,
                                                         'obj_apps':obj_apps,
                                                         'obj_events':obj_events,
                                                        })
            else:
                return render(request, 'report_single.html', {'massage': 'ورودی ها به درستی وارد نشده است',
                                                              'obj_apps': obj_apps,
                                                              'obj_events': obj_events,
                                                              })

        else:
            return render(request,'report_single.html',{'massage':'این کد فعال سازی معتبر نمی باشد ',
                                                     'obj_apps':obj_apps,
                                                     'obj_events':obj_events,
                                                    })

    else:
        return render(request, page, {'massage': massage,
                               'obj_apps': obj_apps,
                               })


