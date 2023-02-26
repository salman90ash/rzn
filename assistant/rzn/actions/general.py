import os
import shutil


def type_cab_mi_or_not(type_id: int) -> bool:
    if type_id == 1 or type_id == 2 or type_id == 3:
        return True
    return False


def get_title_task_details(title, task_type_id, task_type_title, number, date):
    if task_type_id == 6:
        return f"{title} ({task_type_title} | Исх. № {number} от {date})"
    return f"{title} ({task_type_title} | Вх. № {number} от {date})"


def set_task_info(task, title_details=True):
    title = ''
    date = ''
    if task.data.type.id == 6:
        title = get_title_task_details(task.title, task.data.type.id, task.data.type.title,
                                       task.data.dec_number, task.data.dec_date)
        date = task.data.dec_date
    else:
        title = get_title_task_details(task.title, task.data.type.id, task.data.type.title,
                                       task.data.rzn_number, task.data.rzn_date)
        date = task.data.rzn_date
    if title_details:
        return {
            'id': task.id,
            'title': title,
            'url': task.data.get_url_for_browser(),
            'date': date,
            'date_created': task.date_created
        }
    return {
        'id': task.id,
        'title': f"{task.title} ({task.data.type.title})",
        'url': task.data.get_url_for_browser(),
        'date': date,
        'date_created': task.date_created
    }


def clear_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
