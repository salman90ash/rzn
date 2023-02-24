from assistant.settings import RZN_DOMAIN


def get_url_for_py(rzn_number: str, rzn_date: str) -> str:
    return RZN_DOMAIN + '/services/cab_mi?type_search=1&letters=0&in_doc_num=' + rzn_number + '&in_doc_dt=' + rzn_date


def get_url_for_vird(rzn_number: str, rzn_date: str) -> str:
    return RZN_DOMAIN + '/services/cab_mi?type_search=1&letters=0&in_doc_num=' + rzn_number + '&in_doc_dt=' + rzn_date


def get_url_for_duplicate(rzn_number: str, rzn_date: str) -> str:
    return RZN_DOMAIN + '/services/cab_mi?type_search=4&letters=0&in_doc_num=' + rzn_number + '&in_doc_dt=' + rzn_date


# doc_type=1 - входящий
# doc_type=2 - исходящий
def get_url_for_letters(number: str, date: str, rzn_requisites: bool = False) -> str:
    if rzn_requisites:
        return RZN_DOMAIN + '/services/le?&doc_type=1&doc_num=' + number + '&doc_dt=' + date
    return RZN_DOMAIN + '/services/le?&doc_type=2&doc_num=' + number + '&doc_dt=' + date


def get_url(number: str, date: str, type_id: int) -> str:
    url = ''
    if type_id == 1:
        url = get_url_for_py(number, date)
    elif type_id == 2 or type_id == 3:
        url = get_url_for_letters(number, date, rzn_requisites=True)
    elif type_id == 4:
        url = get_url_for_vird(number, date)
    elif type_id == 5:
        url = get_url_for_duplicate(number, date)
    elif type_id == 6:
        url = get_url_for_letters(number, date)
    return url