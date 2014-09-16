# -*- encoding: UTF-8 -*-

from django_tables2 import RequestConfig


def total_table(request, data, table_class):
    amount = dict()
    for key in data[0].keys():
        amount[key] = 0
    for element in data:
        for key in element.keys():
            try:
                amount[key] += element[key]
            except TypeError:
                pass
    table = table_class(data=[amount], orderable=False)
    RequestConfig(request, paginate=False).configure(table)
    return table