from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse
from users.models import CustomUser
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from assistant.settings import API_TG_TOKEN
import json


# Create your views here.

@csrf_exempt
def tg_create_user(request, token):
    global API_TG_TOKEN
    if API_TG_TOKEN == token:
        tg_chat_id = request.POST.get("tg_chat_id")
        tg_username = request.POST.get("tg_username")
        tg_first_name = request.POST.get("tg_first_name")
        tg_last_name = request.POST.get("tg_last_name")
        username = 'username_' + str(tg_chat_id)
        user = CustomUser(username=username, tg_chat_id=tg_chat_id)
        if tg_username:
            user.tg_username = tg_username

        if tg_first_name:
            user.tg_first_name = tg_first_name

        if tg_last_name:
            user.tg_last_name = tg_last_name

        try:
            user.save()
            return HttpResponse(user)
        except IntegrityError:
            return HttpResponse(False)


@csrf_exempt
def tg_get_user(request, token, tg_chat_id):
    global API_TG_TOKEN
    if API_TG_TOKEN == token:
        try:
            user = CustomUser.objects.get(tg_chat_id=tg_chat_id)
            user_dict = {
                "id": user.id,
                "tg_chat_id": user.tg_chat_id,
                "setting_task_title": user.setting_task_title,
                "setting_task_sorting": user.setting_task_sorting,
                "setting_screenshot": user.setting_screenshot
            }
            return HttpResponse(json.dumps(user_dict), content_type="application/json")
        except ObjectDoesNotExist:
            return HttpResponse(False)


@csrf_exempt
def tg_set_task_sorting(request, token, tg_chat_id):
    global API_TG_TOKEN
    if API_TG_TOKEN == token:
        try:
            setting_task_sorting = request.POST.get("setting_task_sorting")
            user = CustomUser.objects.get(tg_chat_id=tg_chat_id)
            user.setting_task_sorting = setting_task_sorting
            user.save()
            user_dict = {
                "setting_task_sorting": setting_task_sorting
            }
            return HttpResponse(json.dumps(user_dict), content_type="application/json")
        except ObjectDoesNotExist:
            return HttpResponse(False)


@csrf_exempt
def tg_set_task_detail(request, token, tg_chat_id):
    global API_TG_TOKEN
    if API_TG_TOKEN == token:
        if request.method == "POST":
            value = request.POST.get("setting_task_title")
            if value.lower() == "true" or value.lower() == "True":
                value = True
            else:
                value = False
            user = CustomUser.objects.get(tg_chat_id=tg_chat_id)
            user.setting_task_title = value
            user.save()
            return HttpResponse(json.dumps({"setting_task_title": f"{user.setting_task_title}"}),
                                content_type="application/json")


@csrf_exempt
def tg_set_setting_screenshot(request, token, tg_chat_id):
    global API_TG_TOKEN
    if API_TG_TOKEN == token:
        if request.method == "POST":
            value = request.POST.get("setting_screenshot")
            if value.lower() == "true" or value.lower() == "True":
                value = True
            else:
                value = False
            user = CustomUser.objects.get(tg_chat_id=tg_chat_id)
            user.setting_screenshot = value
            user.save()
            return HttpResponse(json.dumps({"setting_screenshot": f"{user.setting_screenshot}"}),
                                content_type="application/json")
