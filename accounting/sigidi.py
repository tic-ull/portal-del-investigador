# -*- encoding: UTF-8 -*-

from django.db import connections
from django.conf import settings as st
from enum import Enum, IntEnum
import re


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


class SigidiTables(Enum):
    PROJECTS = 'OBJ_2216'
    CONVENIOS = 'OBJ_2215'


class SigidiConnection:

    dataid = 'select "DATAID" from "OBJ_2275" where "DNI"=\'{0}\''

    proid = 'select "PROID" from "NIV_PRODUCTS" where "PRODATAID"' \
            ' in (' + dataid + ')'

    vrid = 'select "VRID" from "NIV_VALUES_REF" where "VRTARGETID"' \
           ' in (' + proid + ')'

    permission_query = 'select "CODIGO", "CONT_KEY", "ALLOW_CONTAB_RES", ' \
                       '"ALLOW_CONTAB_LIST", "NAME" from "%(table)s" where '

    all_entities_query = 'select "CODIGO", "CONT_KEY", "NAME"' \
                         ' from "%(table)s" order by "NAME"'

    one_entity_query = 'select "CODIGO", "CONT_KEY", "NAME" from "%(table)s"' \
                       'where "CODIGO"=\'%(entity)s\''

    permission_query_end = '"{0}" in ({1})'

    dataids_from_username = 'select "DATAID" from "OBJ_2274"' \
                            ' where "USERNAME"=\'{0}\''

    product_from_dataids = 'select "PROID" from "NIV_PRODUCTS"' \
                           ' where "PRODATAID"' \
                           ' in (' + dataids_from_username + ')'

    user_categories_query = 'select "REL_PC_CATEGORYID" from "NIV_PROCATREL"' \
                            ' where "REL_PC_PRODUCTID"' \
                            ' in (' + product_from_dataids + ')'

    #dataids_from_obj_2275 = 'select "DATAID" from "OBJ_2275"' \
    #                        ' where "DNI"=\'{0}\''

    refs_from_dataids = 'select "VRID" from "NIV_VALUES_REF"' \
                        ' where "VRTARGETDATAID"' \
                        ' in (' + dataid + ')'

    projects_where_is_ip_query = 'select "CODIGO", "CONT_KEY", "NAME"' \
                                 ' from "OBJ_2216" where "IP_ULL"' \
                                 ' in (' + refs_from_dataids + ')'

    projects_permissions = set([
        SigidiCategories.SUPERUSUARIO,
        SigidiCategories.GESTOR_PROYECTOS,
        SigidiCategories.GESTOR_PROYECTOS_SOLO_LECTURA])

    convenios_permissions = set([
        SigidiCategories.SUPERUSUARIO,
        SigidiCategories.GESTOR_CONVENIOS_Y_CONTRATOS,
        SigidiCategories.GESTOR_CONVENIOS_Y_CONTRATOS_SOLO_LECTURA
    ])

    def __init__(self, user):
        self.user = user
        st.DATABASES['sigidi'] = st.SIGIDI_DB
        self.cursor = connections['sigidi'].cursor()
        self.cursor.execute(self.vrid.format(user.profile.documento))
        user_permissions = self.cursor.fetchall()
        user_permissions = re.sub('[\[\]()]|,,', '',
                                  str(user_permissions)).strip(',')
        user_permissions = re.sub(',,', ',', user_permissions)
        if user_permissions == '':
            user_permissions = '0'
        self.user_permissions = user_permissions

    def _make_query(self, query, table=None):
        """Makes a query and returns the result"""
        self.cursor.execute(query % {'table': table})
        return self.cursor.fetchall()

    def _make_query_dict(self, query, table=None):
        """Makes a query and returns the result in a dictionary"""
        self.cursor.execute(query % {'table': table})
        desc = self.cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in self.cursor.fetchall()
        ]

    def _query_entity(self, permissions, table):
        """Builds dynamically query to get projects for a user"""
        sentence = self.permission_query
        for permission in permissions:
            sentence += self.permission_query_end.format(
                permission.value, self.user_permissions) + " OR "
        sentence = sentence[:-4]  # Remove the last OR
        return self._make_query_dict(sentence, table)

    def _codes_to_categories(self, codes):
        roles = []
        for code in codes:
            roles.append(SigidiCategories(code[0]))
        return roles

    def _has_any_role(self, needed):
        roles = self.get_user_roles()
        if roles.intersection(needed):
            return True
        return False

    def _get_user_entities(self, entity_type):
        """Get the projects that the user has permissions to see"""
        entities = self._query_entity(
            [SigidiPermissions.CONTAB_RES, SigidiPermissions.CONTAB_LIST],
            entity_type)
        return entities

    def _can_view_all_entities(self, entity_type):
        if entity_type == SigidiTables.PROJECTS:
            return self.can_view_all_projects()
        else:
            return self.can_view_all_convenios()

    def _get_entity(self, entity, entity_type, permission=None):
        """
        Gets the specified project if the user has permission. If permission
        is not specified returns project where user has any permission
        """

        if self._can_view_all_entities(entity_type):
            entities = self._make_query_dict(
                self.one_entity_query % {'entity': entity,
                                         'table': entity_type})
            if entities:
                entity = entities[0]
                entity[SigidiPermissions.CONTAB_RES.value] = True
                entity[SigidiPermissions.CONTAB_LIST.value] = True
                return entity

        if permission is None:
            permission = [SigidiPermissions.CONTAB_LIST,
                          SigidiPermissions.CONTAB_RES]
        else:
            permission = [permission]

        # We ask to database for the projects that the user
        # has permissions for
        entities = self._query_entity(permission, entity_type)

        # We filter the project that was asked for
        for proj in entities:
            if proj['CODIGO'] == entity:
                return proj
        return False

    def _get_projects_where_is_ip(self):
        projects = self._make_query_dict(self.projects_where_is_ip_query.format(
            '78637064H'))
        for project in projects:
            project[SigidiPermissions.CONTAB_RES.value] = True
            project[SigidiPermissions.CONTAB_LIST.value] = True
        return projects

    def get_project(self, project_id, permission=None):
        # We ask first for the ip, because if the user is the ip
        # then he has all permissions over the project
        projects_ip = self._get_projects_where_is_ip()
        for project_ip in projects_ip:
            if project_ip['CODIGO'] == project_id:
                return project_ip
        project_perm = self._get_entity(project_id, SigidiTables.PROJECTS.value)
        return project_perm

    def get_convenio(self, convenio, permission=None):
        return self._get_entity(convenio, SigidiTables.CONVENIOS.value)

    def can_contab_res(self, project):
        return bool(self.get_project(project, SigidiPermissions.CONTAB_RES))

    def can_contab_list(self, project):
        return bool(self.get_project(project, SigidiPermissions.CONTAB_LIST))

    def get_user_roles(self):
        roles = self._make_query(self.user_categories_query.format(
            self.user.username))
        return set(self._codes_to_categories(roles))

    def can_view_all_projects(self):
        return self._has_any_role(self.projects_permissions)

    def can_view_all_convenios(self):
        return self._has_any_role(self.convenios_permissions)

    def get_all_projects(self):
        if self.can_view_all_projects():
            return self._make_query_dict(self.all_entities_query % {
                'table': SigidiTables.PROJECTS.value})
        return None

    def get_all_convenios(self):
        if self.can_view_all_convenios():
            return self._make_query_dict(self.all_entities_query % {
                'table': SigidiTables.CONVENIOS.value})
        return None

    def get_user_projects(self):
        projects_permission = self._get_user_entities(
            SigidiTables.PROJECTS.value)
        projects_ip = self._get_projects_where_is_ip()
        for pp in projects_permission:
            for pi in projects_ip:
                if pp['CODIGO'] == pi['CODIGO']:
                    projects_permission.remove(pp)
        return projects_permission + projects_ip

    def get_user_convenios(self):
        return self._get_user_entities(SigidiTables.CONVENIOS.value)
