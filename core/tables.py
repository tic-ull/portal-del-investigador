# -*- encoding: UTF-8 -*-

import django_tables2 as tables


class Table(tables.Table):

    def __init__(self, *args, **kwargs):
        columns = kwargs.pop('columns', None)
        super(Table, self).__init__(*args, **kwargs)
        if columns is None:
            return
        for i in range(0, len(self.columns.all())):
            try:
                self.columns[i].column.attrs = columns[i]
            except KeyError:
                self.columns[i].column.visible = False
