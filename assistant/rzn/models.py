from django.db import models

import assistant.settings
from assistant.settings import AUTH_USER_MODEL, RZN_DOMAIN
from rzn.actions.completeness import check_cab_mi, check_le
from rzn.actions.general import type_cab_mi_or_not
from rzn.actions.key import get_key_cab_mi, get_key_le
from rzn.actions.web import get_page, website_availability_check, input_data, get_html, close_webdriver, \
    get_page_screenshot
from pathlib import Path


# Create your models here.

class Tasks(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    data = models.ForeignKey('TasksData', on_delete=models.CASCADE, verbose_name='Сведения')
    is_active = models.BooleanField(default=True, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        res = f"{self.title} ({self.data.type.title})"
        if self.data.rzn_number is not None:
            res = res + f" number={self.data.rzn_number}"
        if self.data.rzn_date is not None:
            res = res + f" date={self.data.rzn_date}"
        if self.data.dec_number is not None:
            res = res + f" dec_number={self.data.dec_number}"
        if self.data.dec_date is not None:
            res = res + f" dec_date={self.data.dec_date}"
        return res


class TasksType(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование')
    is_active = models.BooleanField(default=True, blank=True, verbose_name='Активировать')

    def __str__(self):
        return self.title


class TasksNotice(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование')
    is_active = models.BooleanField(default=True, blank=True, verbose_name='Активировать')

    def __str__(self):
        return self.title


class TasksData(models.Model):
    rzn_number = models.CharField(max_length=255, verbose_name='Вх. номер', null=True)
    rzn_date = models.CharField(max_length=255, verbose_name='Вх. дата', null=True)
    dec_number = models.CharField(max_length=255, verbose_name='Исх. номер', null=True)
    dec_date = models.CharField(max_length=255, verbose_name='Исх. дата', null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)
    date_UPD = models.DateTimeField(auto_now=True, verbose_name='Дата обновления', null=True)
    notice = models.ForeignKey('TasksNotice', on_delete=models.CASCADE, null=True)
    type = models.ForeignKey('TasksType', on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', null=True)

    def __str__(self):
        res = f"id={self.pk} type={self.type.title}"
        if self.rzn_number is not None:
            res = res + f" number={self.rzn_number}"
        if self.rzn_date is not None:
            res = res + f" date={self.rzn_date}"
        if self.dec_number is not None:
            res = res + f" dec_number={self.dec_number}"
        if self.dec_date is not None:
            res = res + f" dec_date={self.dec_date}"
        return res

    def get_url_for_parse(self):
        if self.type.id == 1 or self.type.id == 2 or self.type.id == 3:
            return RZN_DOMAIN + '/services/cab_mi'
        elif self.type.id == 4 or self.type.id == 5:
            return RZN_DOMAIN + '/services/le'

    def get_url_for_browser(self):
        if self.type.id == 1 or self.type.id == 2:
            return RZN_DOMAIN + \
                   '/services/cab_mi?type_search=1&letters=0&in_doc_num=' + \
                   self.rzn_number + '&in_doc_dt=' + self.rzn_date
        elif self.type.id == 3:
            return RZN_DOMAIN + \
                   '/services/cab_mi?type_search=4&letters=0&in_doc_num=' + \
                   self.rzn_number + '&in_doc_dt=' + self.rzn_date
        elif self.type.id == 4:
            return RZN_DOMAIN + '/services/le?&doc_type=1&doc_num=' + self.rzn_number + '&doc_dt=' + self.rzn_date
        elif self.type.id == 5:
            return RZN_DOMAIN + '/services/le?&doc_type=2&doc_num=' + self.dec_number + '&doc_dt=' + self.dec_date

    def get_page_html(self):
        chrome = get_page(
            url=self.get_url_for_parse(),
            proxy=True,
            background=True
        )
        # if website_availability_check(chrome):
        input_data(chrome, self)
        html = get_html(chrome)
        path = f"{Path.home()}{assistant.settings.PATH_SCR}"
        get_page_screenshot(chrome, path, self.pk)
        close_webdriver(chrome)
        return html
        # else:
        #     return ''

    def get_key(self):
        html = self.get_page_html()
        if html == '':
            return ''
        else:
            if type_cab_mi_or_not(self.type.id):
                return get_key_cab_mi(html)
            return get_key_le(html)


class TasksKey(models.Model):
    value = models.JSONField(default={}, blank=True, verbose_name='Ключ')
    date_create = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)
    data = models.ForeignKey('TasksData', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.value=}, {self.data=}"

    def compare(self, other):
        if other.value == '':
            return 1
        else:
            if self.value == '':
                return 2
            else:
                if self == other:
                    for i in range(len(self.value)):
                        if self.value[i] != other.value[i]:
                            return 2  # Обновилась информация на сайте.
                        # print(f"{self.value[i]} == {other.value[i]}")
                elif self < other:
                    return 3  # Увеличилось количество строк на сайте.
                elif self > other:
                    return 4  # Уменьшилось количество строк.
        return 1

    def __eq__(self, other):
        return len(self.value) == len(other.value)

    def __lt__(self, other):
        return len(self.value) < len(other.value)

    def __gt__(self, other):
        return len(self.value) > len(other.value)

    def completeness_check(self, type_id):
        if type_cab_mi_or_not(type_id):
            return check_cab_mi(self)
        return check_le(self)
