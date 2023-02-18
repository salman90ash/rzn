"""assistant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from tg_bot.views import tg_create_user, tg_get_user, tg_set_task_sorting, tg_set_task_detail, tg_set_setting_screenshot

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tg/api/v1/<str:token>/users/', tg_create_user),
    path('tg/api/v1/<str:token>/users/<int:tg_chat_id>/', tg_get_user),
    path('tg/api/v1/<str:token>/users/<int:tg_chat_id>/setTaskSorting/', tg_set_task_sorting),
    path('tg/api/v1/<str:token>/users/<int:tg_chat_id>/setTaskDetail/', tg_set_task_detail),
    path('tg/api/v1/<str:token>/users/<int:tg_chat_id>/setScreenshot/', tg_set_setting_screenshot),
]
