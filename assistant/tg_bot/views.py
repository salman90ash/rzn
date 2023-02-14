from django.shortcuts import render
from django.http import HttpResponse
from users.models import CustomUser
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from assistant.settings import API_TG_TOKEN

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
