from rzn.actions.general import type_cab_mi_or_not

mark_PY_negative = 'об отказе в регистрации'
mark_PY_positive = 'ыдано Регистрационное удостоверение'

# Принято решение об отказе во внесении изменений в документы
# Принято решение о внесении изменений в документы
mark_VIRD = 'Принято решение'

# Принято решение о выдаче дубликата регистрационного
mark_duplicate = 'Принято решение'

mark_zamena_blanka = 'Принято решение'

mark_le = ' от '


def get_last_row_cam_mi(data: list):
    return data[len(data) - 1]


def get_last_row_le(data: list):
    return data[len(data) - 1]


def validate_last_row_cab_mi(row: list):
    for txt in row:
        if mark_PY_positive in txt or mark_PY_negative in txt:
            return True  # Задача завершена
    return False  # Задача в работе


def validate_last_row_le(row: str):
    if mark_le in row:
        return True  # Задача завершена
    return False  # Задача в работе


def check_cab_mi(key):
    data = key.value
    last_row = get_last_row_cam_mi(data)
    return validate_last_row_cab_mi(last_row)


def check_le(key):
    data = key.value
    last_row = get_last_row_le(data)
    return validate_last_row_le(last_row)


# def check(key, type_id: int):
#     if type_cab_mi_or_not(type_id):
#         return check_cab_mi(key)
#     return check_le(key)
