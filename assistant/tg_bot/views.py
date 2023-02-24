from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse
from rzn.models import TasksData, TasksNotice, TasksType, TasksKey, Tasks
from users.models import CustomUser
from django.db import IntegrityError, transaction
from django.views.decorators.csrf import csrf_exempt
from assistant.settings import API_TG_TOKEN
from rzn.actions.general import set_task_info
import json
import datetime


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
def tg_set_sorting(request, token, tg_chat_id):
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
def tg_set_task_title(request, token, tg_chat_id):
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


@csrf_exempt
@transaction.atomic
def tg_create_task(request, token):
    global API_TG_TOKEN
    if API_TG_TOKEN == token:
        tg_chat_id = request.POST.get("tg_chat_id")
        type_id = int(request.POST.get("type"))
        title = request.POST.get("name_md")
        number = request.POST.get("number")
        date = request.POST.get("date")

        if type_id == 5:  # если по исх.
            data = TasksData.objects.filter(type_id=type_id, dec_number=number, dec_date=date)
        else:  # если по вх.
            data = TasksData.objects.filter(type_id=type_id, rzn_number=number, rzn_date=date)

        if data.count() == 1:
            data = data[0]
        else:
            notice = TasksNotice.objects.get(id=1)

            if type_id == 5:  # если по исх.
                type = TasksType.objects.get(id=type_id)
                data = TasksData(dec_number=number,
                                 dec_date=date,
                                 url='',
                                 notice=notice,
                                 type=type
                                 )
                data.save()
            else:  # если по вх.
                type = TasksType.objects.get(id=type_id)
                data = TasksData(rzn_number=number,
                                 rzn_date=date,
                                 url='',
                                 notice=notice,
                                 type=type
                                 )
                data.save()

            key_value = data.get_key()
            key = TasksKey(value=key_value,
                           data=data
                           )
            key.save()

        user = CustomUser.objects.get(tg_chat_id=tg_chat_id)
        task = Tasks(title=title,
                     user=user,
                     data=data)
        task.save()
        return HttpResponse(task.__str__())


@csrf_exempt
@transaction.atomic
def tg_list_tasks(request, token, tg_chat_id):
    global API_TG_TOKEN
    if API_TG_TOKEN == token:
        user = CustomUser.objects.get(tg_chat_id=tg_chat_id)
        tasks = Tasks.objects.filter(user=user.id, is_active=True)
        list_result = []
        setting_task_title = user.setting_task_title
        if setting_task_title:
            for task in tasks:
                list_result.append(set_task_info(task))
        else:
            for task in tasks:
                list_result.append(set_task_info(task, False))
        setting_task_sorting = user.setting_task_sorting
        new_list = []
        if 'title' in setting_task_sorting:
            if 'ASC' in setting_task_sorting:
                new_list = sorted(list_result, key=lambda x: x['title'])
            else:
                new_list = sorted(list_result, key=lambda x: x['title'], reverse=True)
        elif 'date' in setting_task_sorting:
            if 'ASC' in setting_task_sorting:
                new_list = sorted(list_result, key=lambda x: datetime.datetime.strptime(x['date'], '%d.%m.%Y').date())
            else:
                new_list = sorted(list_result, key=lambda x: datetime.datetime.strptime(x['date'], '%d.%m.%Y').date(),
                                  reverse=True)
        elif 'date_created' in setting_task_sorting:
            if 'ASC' in setting_task_sorting:
                new_list = sorted(list_result, key=lambda x: x['date_created'])
            else:
                new_list = sorted(list_result, key=lambda x: x['date_created'], reverse=True)

        for obj in new_list:
            if 'date' in obj:
                del obj['date']
            if 'date_created' in obj:
                del obj['date_created']
        result = json.dumps(new_list)
        return HttpResponse(result, content_type="application/json")


@csrf_exempt
def tg_del_task(request, token, task_id):
    global API_TG_TOKEN
    if API_TG_TOKEN == token:
        try:
            task = Tasks.objects.get(id=task_id)
            task.is_active = False
            task.save()
            data_id = task.data.pk
            tasks = Tasks.objects.filter(data=data_id, is_active=True)
            if len(tasks) == 0:
                data = TasksData.objects.get(id=data_id)
                data.is_active = False
                data.save()
            result_dict = {
                "title": task.title,
                "type_id": task.data.type.id,
                "type_title": task.data.type.title,
            }
            if task.data.type.id != 6:
                result_dict['number'] = task.data.rzn_number
                result_dict['date'] = task.data.rzn_date
            else:
                result_dict['number'] = task.data.dec_number
                result_dict['date'] = task.data.dec_date
            result = json.dumps(result_dict)
            return HttpResponse(result, content_type="application/json")
        except ObjectDoesNotExist:
            return HttpResponse(False)


@csrf_exempt
def tg_update_tasks(request, token):
    global API_TG_TOKEN
    if API_TG_TOKEN == token:
        objs = TasksData.objects.filter(is_active=True, completed=False, notice=1)
        for obj in objs:
            key = TasksKey.objects.get(is_active=True, data=obj.pk)
            new_key: TasksKey = TasksKey(value=obj.get_key())
            notice_id = key.compare(new_key)
            if notice_id > 1:
                key.is_active = False
                key.save()
                new_key.data = obj
                new_key.save()
                notice = TasksNotice.objects.get(pk=notice_id)
                obj.notice = notice
                obj.save()
        result = json.dumps({'answer': 'ok'})
        return HttpResponse(result, content_type="application/json")
