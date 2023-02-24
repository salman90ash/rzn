from rzn.actions.general import type_cab_mi_or_not
from bs4 import BeautifulSoup


def get_table_of_cab_mi(html: str) -> str:
    soup = BeautifulSoup(html, 'lxml')
    return soup.find('div', class_='m-cabinet-results-table').text.strip()


def empty_check_table_cab_mi(html: str) -> bool:
    soup = BeautifulSoup(html, 'lxml')
    page = soup.find('div', {"class": "form-additional"})
    if page is None:
        return False
    return True


def parse_table_cab_mi(table: str) -> list:
    rows = table.split('\n\n')
    list_rows = [row[1:].split('\n') for row in rows if row != '' or row.find('\n') != -1]
    return list_rows


def get_key_cab_mi(html: str):
    if empty_check_table_cab_mi(html):
        return ''
    else:
        table = get_table_of_cab_mi(html)
        return parse_table_cab_mi(table)


def get_table_of_le(html: str) -> str:
    soup = BeautifulSoup(html, 'lxml')
    return soup.find('div', class_='m-cabinet-results-table').text.strip()


def empty_check_table_le(html: str) -> bool:
    soup = BeautifulSoup(html, 'lxml')
    page = soup.find('div', {"class": "form-additional"}).find('span')
    if page is None:
        return False
    return True


def parse_table_le(table: str) -> list:
    return [row for row in table.split('\n') if row != '' or row.find('\n') != -1]


def get_key_le(html: str):
    if empty_check_table_le(html):
        return ''
    else:
        table = get_table_of_le(html)
        return parse_table_le(table)


def check_type_le(type_id: int) -> bool:
    if type_id == 3:
        return True  # Обращение по вх.
    return False


def get_key(html, type_id):
    if check_cab_mi(type_id):
        return get_key_cab_mi(html)
    return get_key_le(html)
