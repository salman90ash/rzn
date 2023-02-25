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

from tg_bot.views import tg_create_user, tg_get_user, tg_setting_sorting, tg_set_task_title, \
    tg_set_setting_screenshot, tg_create_task, tg_list_tasks, tg_del_task, tg_update_tasks, tg_send_updates, \
    tg_update_task_after_send_notif, check_rzn_accessibility

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tg/api/v1/<str:token>/users/', tg_create_user),
    path('tg/api/v1/<str:token>/users/<int:tg_chat_id>/', tg_get_user),
    path('tg/api/v1/<str:token>/users/<int:tg_chat_id>/settingTaskSorting/', tg_setting_sorting),
    path('tg/api/v1/<str:token>/users/<int:tg_chat_id>/setTaskTitle/', tg_set_task_title),
    path('tg/api/v1/<str:token>/users/<int:tg_chat_id>/setScreenshot/', tg_set_setting_screenshot),
    path('tg/api/v1/<str:token>/tasks/', tg_create_task),
    path('tg/api/v1/<str:token>/tasks/<int:tg_chat_id>/', tg_list_tasks),
    path('tg/api/v1/<str:token>/tasks/<int:task_id>/del/', tg_del_task),
    path('tg/api/v1/<str:token>/tasks/updates/', tg_update_tasks),
    path('tg/api/v1/<str:token>/tasks/sendUpdates/', tg_send_updates),
    path('tg/api/v1/<str:token>/tasks/updateTaskNotif/<int:task_data_id>/', tg_update_task_after_send_notif),
    path('tg/api/v1/<str:token>/rznAccessibility/', check_rzn_accessibility),
]
