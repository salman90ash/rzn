from datetime import datetime
from pathlib import Path

import assistant
from rzn.actions.general import clear_folder
from rzn.models import TasksData, TasksKey, TasksNotice


def my_job():
    now = datetime.now()
    print(now.strftime("%m/%d/%Y, %H:%M:%S"))


def my_updates():
    path = f"{Path.home()}{assistant.settings.PATH_SCR}"
    clear_folder(path)
    tasks_data = TasksData.objects.filter(is_active=True, notice=1).order_by('id')
    for data in tasks_data:
        print(data)
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
