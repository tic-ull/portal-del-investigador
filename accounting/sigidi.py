# -*- encoding: UTF-8 -*-

from django.db import connections
import re
import django.conf as conf
from enum import Enum, IntEnum


class SigidiPermissions(Enum):
    CONTAB_RES = "ALLOW_CONTAB_RES"
    CONTAB_LIST = "ALLOW_CONTAB_LIST"

class SigidiCategories(IntEnum):
    SUPERUSUARIO = 1
    ADMINISTRADOR_PROYECTOS = 2
    GESTOR_PROYECTOS = 3
    GESTOR_PROYECTOS_SOLO_LECTURA = 1243
    ADMINISTRADOR_CONVENIOS_Y_CONTRATOS = 15
    GESTOR_CONVENIOS_Y_CONTRATOS = 17
    GESTOR_CONVENIOS_Y_CONTRATOS_SOLO_LECTURA = 1244
    ADMINISTRADOR_CVN = 1275
    GESTOR_CVN = 1252
    GESTOR_CVN_SOLO_LECTURA = 1253
    AUXILIAR = 30


class SigidiConnection:

    dataid = 'select "DATAID" from "OBJ_2275" where "DNI"=\'{0}\''

    proid = 'select "PROID" from "NIV_PRODUCTS" where "PRODATAID"' \
            ' in (' + dataid + ')'

    vrid = 'select "VRID" from "NIV_VALUES_REF" where "VRTARGETID"' \
           ' in (' + proid + ')'

    permission_query = 'select "CODIGO", "CONT_KEY", "ALLOW_CONTAB_RES", ' \
                       '"ALLOW_CONTAB_LIST", "NAME" from "OBJ_2216" where '

    all_projects_query = 'select "CODIGO", "CONT_KEY", "NAME" from "OBJ_2216"' \
                         ' order by "NAME"'

    permission_query_end = '"{0}" in ({1})'

    dataids_from_username = 'select "DATAID" from "OBJ_2274"' \
                            ' where "USERNAME"=\'{0}\''

    product_from_dataids = 'select "PROID" from "NIV_PRODUCTS"' \
                           ' where "PRODATAID"' \
                           ' in (' + dataids_from_username + ')'

    user_categories_query = 'select "REL_PC_CATEGORYID" from "NIV_PROCATREL"' \
                            ' where "REL_PC_PRODUCTID"' \
                            ' in (' + product_from_dataids + ')'

    projects_permissions = set([SigidiCategories.SUPERUSUARIO,
                                SigidiCategories.ADMINISTRADOR_PROYECTOS,
                                SigidiCategories.GESTOR_PROYECTOS,
                                SigidiCategories.GESTOR_PROYECTOS_SOLO_LECTURA])

    def __init__(self, user):
        self.user = user
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

    def _make_query(self, query):
        '''Makes a query and returns the result'''
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def _make_query_dict(self, query):
        '''Makes a query and returns the result in a dictionary'''
        self.cursor.execute(query)
        desc = self.cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in self.cursor.fetchall()
        ]

    def _query_projects(self, permissions):
        '''Builds dynamically query to get projects for a user'''
        sentence = self.permission_query
        for permission in permissions:
            sentence += self.permission_query_end.format(
                permission.value, self.user_permissions) + " OR "
        sentence = sentence[:-4] # Remove the last OR
        return self._make_query_dict(sentence)

    def _codes_to_categories(self, codes):
        roles = []
        for code in codes:
            roles.append(SigidiCategories(code[0]))
        return roles

    def get_projects(self):
        '''Get the projects that the user has permissions to see'''
        projects = self._query_projects(
            [SigidiPermissions.CONTAB_RES, SigidiPermissions.CONTAB_LIST])
        return projects

    def get_project(self, project, permission=None):
        '''
        Gets the specified project if the user has permission. If permission
        is not specified returns project where user has any permission
        '''

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

    def get_user_roles(self):
        roles = self._make_query(self.user_categories_query.format(
            self.user.username))
        return set(self._codes_to_categories(roles))

    def can_view_all_projects(self):
        roles = self.get_user_roles()
        if roles.intersection(self.projects_permissions):
            return True
        return False

    def get_all_projects(self):
        if self.can_view_all_projects():
            return self._make_query_dict(self.all_projects_query)
        return None