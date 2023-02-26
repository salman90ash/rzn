from pathlib import Path

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse

import assistant.settings
from rzn.models import TasksData, TasksNotice, TasksType, TasksKey, Tasks
from users.models import CustomUser
from django.db import IntegrityError, transaction
from django.views.decorators.csrf import csrf_exempt
from assistant.settings import API_TG_TOKEN
from rzn.actions.general import set_task_info, clear_folder
from django.core import serializers
import json
import datetime
import time


# Create your views here.

@csrf_exempt
def tg_create_user(request, token):
    global API_TG_TOKEN
    if API_TG_TOKEN == token:
        if request.method == "POST":
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
        elif request.method == "GET":
            users = CustomUser.objects.all()
            res_list = []
            for user in users:
                res_list.append(user.tg_chat_id)
            result = json.dumps(res_list)
            return HttpResponse(result, content_type="application/json")
    else:
        print(f"error value API_TG_TOKEN")
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
def tg_setting_sorting(request, token, tg_chat_id):
    if API_TG_TOKEN == token:
        if request.method == "POST":
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
        elif request.method == "GET":
            try:
                user = CustomUser.objects.get(tg_chat_id=tg_chat_id)
                user_dict = {
                    "setting_task_sorting": user.setting_task_sorting
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
        elif request.method == "GET":
            user = CustomUser.objects.get(tg_chat_id=tg_chat_id)
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
        elif request.method == "GET":
            user = CustomUser.objects.get(tg_chat_id=tg_chat_id)
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
                                 notice=notice,
                                 type=type
                                 )
                data.save()
            else:  # если по вх.
                type = TasksType.objects.get(id=type_id)
                data = TasksData(rzn_number=number,
                                 rzn_date=date,
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
        path = f"{Path.home()}{assistant.settings.PATH_SCR}"
        clear_folder(path)
        tasks_data = TasksData.objects.filter(is_active=True, completed=False, notice=1)
        for data in tasks_data:
            key = TasksKey.objects.get(is_active=True, data=data.pk)
            new_key: TasksKey = TasksKey(value=data.get_key())
            notice_id = key.compare(new_key)
            if notice_id > 1:
                # добавление ключа и смена статуса у старого ключа
                new_key.data = data
                new_key.save()
                key.is_active = False
                key.save()

                # проверка на завершенность задачи, метод возвращает True || False
                completeness = new_key.completeness_check(data.type.id)
                if completeness:
                    data.notice_id = TasksNotice.objects.get(pk=5)
                    data.is_active = False
                else:
                    data.notice = TasksNotice.objects.get(pk=notice_id)
                data.save()
        result = json.dumps({'answer': 'ok'})
        return HttpResponse(result, content_type="application/json")


@csrf_exempt
@transaction.atomic
def tg_send_updates(request, token):
    global API_TG_TOKEN
    if API_TG_TOKEN == token:
        tasks_data = TasksData.objects.filter(notice_id__gte=2)
        list_result = []
        for data in tasks_data:
            tasks = Tasks.objects.filter(data=data.pk)
            for task in tasks:
                notice_text = data.notice.title
                user_tg_chat_id = task.user.tg_chat_id
                title = task.title
                task_type = data.type.title
                user = CustomUser.objects.get(id=task.user_id)
                name = ''
                if len(user.tg_username) > 1:
                    name = "@" + user.tg_username
                if len(user.tg_first_name) > 1:
                    name = name + f" ({user.tg_first_name})"
                    if len(user.tg_last_name) > 1:
                        name = name[:-1] + f" {user.tg_last_name})"
                else:
                    if len(user.tg_last_name) > 1:
                        name = name + f"({user.tg_last_name})"

                dict_result = {
                    'chat_id': user_tg_chat_id,
                    'user': name,
                    'taskdata_id': data.id,
                    'type': task_type,
                    'title': title,
                    'notice': notice_text,
                    'url': data.get_url_for_browser(),
                    'screenshot': task.user.setting_screenshot
                }
                list_result.append(dict_result)
        result = json.dumps(list_result)
        return HttpResponse(result, content_type="application/json")


@csrf_exempt
def tg_update_task_after_send_notif(request, token, task_data_id):
    global API_TG_TOKEN
    if API_TG_TOKEN == token:
        try:
            task_data = TasksData.objects.get(pk=task_data_id)
        except TasksData.DoesNotExist:
            task_data = None
        if task_data is None:
            return HttpResponse(False, content_type="application/json")
        if task_data.notice.pk == 5:
            task_data.is_active = False
            tasks = Tasks.objects.filter(data=task_data.pk)
            for task in tasks:
                task.is_active = False
                task.save()
        notice = TasksNotice.objects.get(pk=1)
        task_data.notice = notice
        task_data.save()
        return HttpResponse(task_data, content_type="application/json")


@csrf_exempt
def check_rzn_accessibility(request, token):
    if API_TG_TOKEN == token:
        accessibility = False
        user_dict = {
            "accessibility": accessibility
        }
        try:
            notice = TasksNotice.objects.get(id=1)
            type = TasksType.objects.get(id=1)
            data = TasksData(rzn_number='77676',
                             rzn_date='28.10.2021',
                             notice=notice,
                             type=type
                             )
            res = data.get_page_html()
            if res != '':
                accessibility = True
                user_dict['accessibility'] = accessibility
        except Exception as e:
            print(e)
        return HttpResponse(json.dumps(user_dict), content_type="application/json")
