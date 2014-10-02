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


class SigidiEntityType(IntEnum):
    PROYECTOS = 0
    CONVENIOS = 1


sigidi_tables = {SigidiEntityType.PROYECTOS: 'OBJ_2216',
                 SigidiEntityType.CONVENIOS: 'OBJ_2215'}


sigidi_dates = {SigidiEntityType.PROYECTOS: 'PROP_CONC_FECHA_ACEPT',
                SigidiEntityType.CONVENIOS: 'FECHA_INICIO'}


class SigidiConnection:

    dataid = 'select "DATAID" from "OBJ_2275" where "DNI"=\'{0}\'' \
             ' and "ISACTIVE"=1'

    proid = 'select "PROID" from "NIV_PRODUCTS" where "PRODATAID"' \
            ' in (' + dataid + ')'

    vrid = 'select "VRID" from "NIV_VALUES_REF" where "VRTARGETID"' \
           ' in (' + proid + ')'

    # Proyectos/Convenios for user with explicit permissions
    permission_query = 'select "CODIGO", "CONT_KEY", "ALLOW_CONTAB_RES", ' \
                       '"ALLOW_CONTAB_LIST", "NAME", "%(fecha_inicio)s",' \
                       ' "IP_ULL" from "%(table)s" where '

    # All Proyectos/Convenios
    all_entities_query = 'select "CODIGO", "CONT_KEY", 1 "ALLOW_CONTAB_RES",' \
                         ' 1 "ALLOW_CONTAB_LIST",' \
                         ' "NAME", "%(fecha_inicio)s", "IP_ULL"' \
                         ' from "%(table)s" order by "NAME"'

    # One Proyecto/Convenio
    one_entity_query = 'select "CODIGO", "CONT_KEY", "IP_ULL",' \
                       ' "NAME", "%(fecha_inicio)s", 1 "ALLOW_CONTAB_RES",' \
                       ' 1 "ALLOW_CONTAB_LIST" from "%(table)s"' \
                       'where "CODIGO"=\'%(entity)s\''

    permission_query_end = '"{0}" in ({1})'

    dataids_from_username = 'select "DATAID" from "OBJ_2274"' \
                            'where "USERNAME"=\'{0}\' and "ISACTIVE"=1 and' \
                            '(("VALID_FROM" is NULL or "VALID_FROM" < NOW())' \
                            'and ("VALID_TO" is NULL or "VALID_TO" > NOW()))'

    product_from_dataids = 'select "PROID" from "NIV_PRODUCTS"' \
                           ' where "PRODATAID"' \
                           ' in (' + dataids_from_username + ')'

    user_categories_query = 'select "REL_PC_CATEGORYID" from "NIV_PROCATREL"' \
                            ' where "REL_PC_PRODUCTID"' \
                            ' in (' + product_from_dataids + ')'

    refs_from_dataids = 'select "VRID" from "NIV_VALUES_REF"' \
                        ' where "VRTARGETDATAID"' \
                        ' in (' + dataid + ')'

    # Proyectos/Convenios where is ip
    entities_where_is_ip_query = 'select "CODIGO", "CONT_KEY", "NAME",' \
                                 ' "IP_ULL", "%(fecha_inicio)s",' \
                                 ' 1 "ALLOW_CONTAB_RES",' \
                                 ' 1 "ALLOW_CONTAB_LIST" ' \
                                 'from "%(table)s" where "IP_ULL"' \
                                 ' in (' + refs_from_dataids + ')'

    macroquery = 'select entities."CODIGO", entities."CONT_KEY",' \
                 ' "OBJ_2275"."NAME" "IP",' \
                 ' entities."NAME", entities."%(fecha_inicio)s" "DATE",' \
                 ' entities."ALLOW_CONTAB_RES", entities."ALLOW_CONTAB_LIST"' \
                 ' from "OBJ_2275" right join "NIV_VALUES_REF"' \
                 ' on "OBJ_2275"."DATAID" = "NIV_VALUES_REF"."VRTARGETDATAID"' \
                 ' right join (%(entities_query)s) entities' \
                 ' on "NIV_VALUES_REF"."VRID" = entities."IP_ULL"' \

    proyectos_permissions = set([
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

    def _query_entity(self, permissions, entity_type):
        """Builds dynamically query to get projects for a user"""
        sentence = self.permission_query
        for permission in permissions:
            sentence += self.permission_query_end.format(
                permission.value, self.user_permissions) + " OR "
        sentence = sentence[:-4]  # Remove the last OR
        subquery = sentence % {'table': sigidi_tables[entity_type],
                               'fecha_inicio': sigidi_dates[entity_type]}
        return self._do_the_macroquery(subquery, sigidi_dates[entity_type])

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

    def _get_entities_where_has_permission(self, entity_type):
        """Get the projects that the user has permissions to see"""
        entities = self._query_entity(
            [SigidiPermissions.CONTAB_RES, SigidiPermissions.CONTAB_LIST],
            entity_type)
        return entities

    def _can_view_all_entities(self, entity_type):
        if entity_type == SigidiEntityType.PROYECTOS:
            return self.can_view_all_projects()
        else:
            return self.can_view_all_convenios()

    def _get_entity_where_has_permission(self, entity, entity_type,
                                         permission=None):
        """
        Gets the specified project if the user has permission. If permission
        is not specified returns project where user has any permission
        """

        date_row = sigidi_dates[entity_type]

        if self._can_view_all_entities(entity_type):
            subquery = self.one_entity_query % {
                'entity': entity, 'table': sigidi_tables[entity_type],
                'fecha_inicio': date_row}
            entities = self._do_the_macroquery(subquery, date_row)
            if entities:
                entity = entities[0]
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

    def _get_entities_where_is_ip(self, entity_type):
        date_row = sigidi_dates[entity_type]
        subquery = self.entities_where_is_ip_query.format(
            self.user.profile.documento) % {'table': sigidi_tables[entity_type],
                                            'fecha_inicio': date_row}
        entities = self._do_the_macroquery(subquery, date_row)
        return entities

    def _get_entity(self, entity_id, entity_type):
        entities_ip = self._get_entities_where_is_ip(entity_type)
        for entity_ip in entities_ip:
            if entity_ip['CODIGO'] == entity_id:
                return entity_ip
        entity_perm = self._get_entity_where_has_permission(entity_id,
                                                             entity_type)
        return entity_perm

    def _do_the_macroquery(self, subquery, date_format):
        return self._make_query_dict(self.macroquery % {
            'entities_query': subquery,
            'fecha_inicio': date_format})

    def get_project(self, project_id):
        return self._get_entity(project_id, SigidiEntityType.PROYECTOS)

    def get_convenio(self, convenio_id):
        return self._get_entity(convenio_id, SigidiEntityType.CONVENIOS)

    def can_contab_res(self, project):
        return bool(self.get_project(project, SigidiPermissions.CONTAB_RES))

    def can_contab_list(self, project):
        return bool(self.get_project(project, SigidiPermissions.CONTAB_LIST))

    def get_user_roles(self):
        roles = self._make_query(self.user_categories_query.format(
            self.user.username))
        return set(self._codes_to_categories(roles))

    def can_view_all_projects(self):
        return self._has_any_role(self.proyectos_permissions)

    def can_view_all_convenios(self):
        return self._has_any_role(self.convenios_permissions)

    def get_all_projects(self):
        if self.can_view_all_projects():
            date_row = sigidi_dates[SigidiEntityType.PROYECTOS]
            entities_query = self.all_entities_query % {
                'table': sigidi_tables[SigidiEntityType.PROYECTOS],
                'fecha_inicio': date_row}
            return self._do_the_macroquery(entities_query, date_row)
        return None

    def get_all_convenios(self):
        if self.can_view_all_convenios():
            date_row = sigidi_dates[SigidiEntityType.CONVENIOS]
            entities_query = self.all_entities_query % {
                'table': sigidi_tables[SigidiEntityType.CONVENIOS],
                'fecha_inicio': date_row}
            return self._do_the_macroquery(entities_query, date_row)
        return None

    def _get_user_entities(self, entity_type):
        entities_permission = self._get_entities_where_has_permission(
            entity_type)
        entities_ip = self._get_entities_where_is_ip(entity_type)
        for ep in entities_permission:
            for ei in entities_ip:
                if ep['CODIGO'] == ei['CODIGO']:
                    entities_permission.remove(ep)
        entities = entities_permission + entities_ip
        return entities

    def get_user_projects(self):
        return self._get_user_entities(SigidiEntityType.PROYECTOS)

    def get_user_convenios(self):
        return self._get_user_entities(SigidiEntityType.CONVENIOS)