# -*- encoding: UTF-8 -*-

from django.db import connections
import re
import django.conf as conf


class SigidiPermissions:
    CONTAB_RES = "ALLOW_CONTAB_RES"
    CONTAB_LIST = "ALLOW_CONTAB_LIST"

class SigidiConnection:

    dataid = 'select "DATAID" from "OBJ_2275" where "DNI"=\'{0}\''

    proid = 'select "PROID" from "NIV_PRODUCTS" where "PRODATAID"' \
            ' in (' + dataid + ')'

    vrid = 'select "VRID" from "NIV_VALUES_REF" where "VRTARGETID"' \
           ' in (' + proid + ')'

    permission_query = 'select "CODIGO", "CONT_KEY", "ALLOW_CONTAB_RES", ' \
                       '"ALLOW_CONTAB_LIST" from "OBJ_2216" where '

    permission_query_end = '"{0}" in ({1})'

    def __init__(self, user):
        conf.settings.DATABASES['sigidi'] = conf.settings.SIGIDI_DB
        self.cursor = connections['sigidi'].cursor()
        self.cursor.execute(self.vrid.format(user.profile.documento))
        user_permissions = self.cursor.fetchall()
        user_permissions = re.sub('[\[\]()]|,,', '',
                                       str(user_permissions)).strip(',')
        user_permissions = re.sub(',,', ',', user_permissions)
        if user_permissions == '':
            user_permissions = '0'
        self.user_permissions = user_permissions

    @staticmethod
    def _dictfetchall(cursor):
        "Returns all rows from a cursor as a dict"
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

    def _query_projects(self, permissions):
        sentence = self.permission_query
        for permission in permissions:
            sentence += self.permission_query_end.format(
                permission,self.user_permissions) + " OR "
        sentence = sentence[:-4] # Remove the last OR
        self.cursor.execute(sentence)
        return self._dictfetchall(self.cursor)

    def get_projects(self):
        projects = self._query_projects(
            [SigidiPermissions.CONTAB_RES, SigidiPermissions.CONTAB_LIST])
        return projects

    def get_project(self, project, permission=None):
        # If the user didnt specify what permission to ask for,
        # we ask for any
        if permission is None:
            permission = [SigidiPermissions.CONTAB_LIST,
                          SigidiPermissions.CONTAB_RES]
        else:
            permission = [permission]

        # We ask to database for the projects that the user
        # has permissions for
        projects = self._query_projects(permission)

        # We filter the project that was asked for
        for proj in projects:
            if proj['CODIGO'] == project:
                return proj
        return False

    def can_contab_res(self, project):
        return bool(self.get_project(project, SigidiPermissions.CONTAB_RES))

    def can_contab_list(self, project):
        return bool(self.get_project(project, SigidiPermissions.CONTAB_LIST))