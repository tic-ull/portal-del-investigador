# -*- encoding: UTF-8 -*-

import django_tables2 as tables

class Table(tables.Table):

    @classmethod
    def create(cls, data, attrs, sortable=True):
        table = cls(data)
        table.sortable = sortable
        for i in range(0, len(table.columns.all())):
            try:
                table.columns[i].column.attrs = attrs[i]
            except KeyError:
                table.columns[i].column.visible = False
        return table

