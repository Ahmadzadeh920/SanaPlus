# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.http import request
from  SanaPlus.models import Apps_tokens_admin,Events_Apps , Apps_tokens_admin
from .models import Record_Events
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render
from django.contrib.auth.models import User, Permission
from datetime import datetime
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from user_agents import parse
import json
from django_user_agents.utils import get_user_agent
from Serializer import (
                 clicked_serialize,
                 Page_Ranking_serialize,
                 Reservation_serializer,
                Seller_serializer,
                Visited_Product_serializer,
                Search_Product_serializer,
                Register_user_serializer,

)

# Create your views here.


def check_Reporting_link(request,username,token_apps,code_Events):
    if username and User.objects.filter(username=username):
        if  Apps_tokens_admin.objects.filter(token=token_apps).exists() and Events_Apps.objects.filter(code=code_Events).exists():
            obj_app=Apps_tokens_admin.objects.get(token=token_apps)
            obj_Events=Events_Apps.objects.get(code=code_Events)
            if obj_Events.apps_events==obj_app:
                return render(request, 'Events/Events.js', {'massage': 'OK'})
            else:
                return render(request, 'Events/Events.js', {'massage': 'این Events مربوط به این اپلیکشن نمی باشد '})

        else:
            return render(request, 'Events/Events.js', {'massage': 'token apps and code Events is not validate'})

    else:
        return render(request,'Events/Events.js', {'massage':'username is none valide'})



@csrf_exempt
def realtime_Reporting_link(request,username,token_apps,code_Events):
    if username and User.objects.filter(username=username):
        if  Apps_tokens_admin.objects.filter(token=token_apps).exists() and Events_Apps.objects.filter(code=code_Events).exists():
            obj_app=Apps_tokens_admin.objects.get(token=token_apps)
            obj_Events=Events_Apps.objects.get(code=code_Events)
            if obj_Events.apps_events==obj_app:

                return render(request, 'Events/real_time.js', {'massage': 'username is none valide'})


            else:
                return JsonResponse({'massage': 'این Events مربوط به این اپلیکشن نمی باشد '}, status=404)

        else:
            return JsonResponse({'massage': 'token apps and code Events is not validate'} , status=404)

    else:
        return JsonResponse({'massage':'username is none valide'}, status=404)



def check_src(src_str):
    src_split = str(src_str).split("/")
    if len(src_split) > 7:
        username = src_split[5]
        # username='admin_21'
        token_app = src_split[6]
        event_app = src_split[7]
        # token_app='fPHQIhAxbaFspOBF5iXMLt0WGjT3xmen'

        if User.objects.filter(username=username).exists():
            obj_user = User.objects.get(username=username)
            if Apps_tokens_admin.objects.filter(token=token_app, user_token=obj_user).exists():
                obj_token = Apps_tokens_admin.objects.get(token=token_app, user_token=obj_user)
                if Events_Apps.objects.filter(apps_events=obj_token, code=event_app).exists():
                    return True, event_app , 200

                else:
                    return False, 'Dose Not Exist Event Code', 404
            return False,'Code apps is not valid', 404
        return False, 'Code User is not valid', 404
    return False,'Adress Script is none',400

@csrf_exempt
def reloads(request):
    src_str = request.GET.get('src_str')
    check, event_code, status = check_src(src_str)
    if check:
        obj_Events=Events_Apps.objects.get(code= event_code)
        if request.GET.get('json_format'):
            clicks_events = request.GET.get('json_format')
            now = datetime.now()
            data={
                'json_fields':json.loads(clicks_events),
                'date_record' : now,
                'Event_id':obj_Events.id,
                }

            serializer=clicked_serialize(data=data)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            else:
                return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({'message':'json_format parameter is not passed '},status=404)
    else:
        return JsonResponse({'message':event_code}, status=status)


#_____________________________
@csrf_exempt
def page_ranking_record(request):
    src_str = request.GET.get('src_str')
    check, event_code, status = check_src(src_str)
    if check:
        obj_Events = Events_Apps.objects.get(code=event_code)
        try:
            json_fields = json.loads(request.GET.get('json_format'))  # must be included Title, URLS , Referrer  in json format
        except ValueError, e:
            return JsonResponse({'message': 'Json Format is not validate '}, status=status)
        data={
            'Event_id':obj_Events.id,
            'date_record' :datetime.now(),
            'json_fields':json_fields
            }
        serializer_page_ranking=Page_Ranking_serialize(data=data)
        if serializer_page_ranking.is_valid():
            serializer_page_ranking.save()
            return JsonResponse(data=serializer_page_ranking.data, status=200)
        else:
            return JsonResponse(serializer_page_ranking.errors, status=400)
    else:
        return JsonResponse({'message': event_code }, status= status)




@csrf_exempt
def Reservetion_Record(request):
    src_str = request.GET.get('src_str')
    check, event_code , status =check_src(src_str)
    if check:
        obj_Events = Events_Apps.objects.get(code=event_code)
        if request.GET.get('json_format'):
            try:
                json_fields=json.loads(request.GET.get('json_format')) # must be included User , Product which reserve , IP_Address , Session_ID in json format
            except ValueError, e:
                return JsonResponse({'message': 'Json_Format Parameter is not validate '}, status=status)
            now=datetime.now()
            id_reserve = request.GET.get('Reservation_id')
            data={
                'Event_id':obj_Events.id,
                'date_record' : now,
                'json_fields':json_fields,
                'Reservation_id': id_reserve,
            }
            serializer=Reservation_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            else:
                return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({'message':'Json_Format Parameter must be passed '}, status=status)

    else:
        return JsonResponse({'message': event_code}, status=status)



@csrf_exempt
def Seller_Record(request):
    src_str = request.GET.get('src_str')
    check, event_code , status =check_src(src_str)
    if check:
        obj_Events = Events_Apps.objects.get(code=event_code)
        if request.GET.get('json_format') and  request.GET.get('Reservation_id'):
            try:
                json_fields=json.loads(request.GET.get('json_format'))
            except ValueError, e:
                return JsonResponse({'message': 'Json_Format Parameter is not validate'}, status=status)
            id_reserve= request.GET.get('Reservation_id')
            now=datetime.now()
            data={
                'Event_id':obj_Events.id,
                'date_record' : now,
                'json_fields':json_fields,
                'Reservation_id': id_reserve,
            }
            serializer=Seller_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            else:
                return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({'message': 'Does Not exist Parameter passed '}, status=status)
    else:
        return JsonResponse({'message':event_code}, status=status)


@csrf_exempt
def Visited_Product_Record(request):
    src_str = request.GET.get('src_str')
    check, event_code , status =check_src(src_str)
    if check:
        obj_Events = Events_Apps.objects.get(code=event_code)
        if request.GET.get('json_format'):
            try:
                json_fields=json.loads(request.GET.get('json_format'))
            except ValueError,e:
                return JsonResponse({'message': 'Json Format is not validate '}, status=status)
            now=datetime.now()
            data={
                'Event_id':obj_Events.id,
                'date_record' : now,
                'json_fields':json_fields,
            }
            serializer=Visited_Product_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            else:
                return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({'message': 'Does Not exist Parameter passed '}, status=status)
    else:
        return JsonResponse({'message':event_code}, status=status)


@csrf_exempt
def Search_Product_Record(request):
    src_str = request.GET.get('src_str')
    check, event_code , status =check_src(src_str)
    if check:
        obj_Events = Events_Apps.objects.get(code=event_code)
        if request.GET.get('json_format'):
            try:
                json_fields=json.loads(request.GET.get('json_format'))
            except ValueError,e:
                return JsonResponse({'message': 'Json Format is not validate '}, status=status)
            now=datetime.now()
            data={
                'Event_id':obj_Events.id,
                'date_record':now,
                'json_fields':json_fields,
            }
            serializer=Search_Product_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            else:
                return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({'message': 'Does Not exist Parameter passed '}, status=status)
    else:
        return JsonResponse({'message':event_code}, status=status)


@csrf_exempt
def Register_user_record(request):
    src_str = request.GET.get('src_str')
    check, event_code, status = check_src(src_str)
    if check:
        obj_Events = Events_Apps.objects.get(code=event_code)
        try:
            json_fields = json.loads(request.GET.get('json_format'))  # must be included Title, URLS , Referrer  in json format
        except ValueError, e:
            return JsonResponse({'message': 'Json Format is not validate '}, status=status)
        data={
            'Event_id':obj_Events.id,
            'date_record' :datetime.now(),
            'json_fields':json_fields
            }
        serializer=Register_user_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data=serializer.data, status=200)
        else:
            return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({'message': event_code }, status= status)


#______________________________________________________ Report Part

