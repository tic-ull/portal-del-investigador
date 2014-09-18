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


def clean_accounting_table(request, data, table_class, role):
    result = list()
    for element in data:
        if 'CONT_KEY' in element and element['CONT_KEY'] is not None:
            result.append(element)
    if len(result):
        result = table_class(result)
        RequestConfig(request, paginate=False).configure(result)
        if not role:  # CONT_KEY column only for managers and admins
            result.columns[2].column.visible = False
    return result
