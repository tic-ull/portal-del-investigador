# -*- encoding: UTF-8 -*-

from .models import Project, Agreement
from django.conf import settings as st
from django.core.exceptions import ObjectDoesNotExist
from django.db import connections
from enum import Enum, IntEnum
import re


def _make_query(cursor, query):
    """Makes a query and returns the result"""
    cursor.execute(query)
    return cursor.fetchall()


def _make_query_dict(cursor, query):
    """Makes a query and returns the result in a dictionary"""
    cursor.execute(query)
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


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


class Sqry:
    """Here we store the Sigidi queries"""

    # vrid_query gets the ids of the user permissions. The returned values can
    # be on any permission rows (SigidiPermissions)
    _dataid = (
        'select "DATAID" from "OBJ_2275" where "DNI"=\'{0}\''
        ' and "ISACTIVE"=1')

    _proid = (
        'select "PROID" from "NIV_PRODUCTS"'
        ' where "PRODATAID" in (' + _dataid + ')')

    vrid_query = (
        'select "VRID" from "NIV_VALUES_REF"'
        ' where "VRTARGETID" in (' + _proid + ')')

    # permission_query Returns Proyectos/Convenios for a user with explicit
    # permissions set (SigidiPermissions)
    permission_query_end = '"{0}" in ({1})'

    permission_query = (
        'select "CODIGO", "CONT_KEY", "ALLOW_CONTAB_RES", '
        ' "ALLOW_CONTAB_LIST", "NAME", "%(fecha_inicio)s",'
        ' "IP_ULL" from "%(table)s" where ')

    # all_entities_query gets all Convenios/Proyectos
    all_entities_query = (
        'select "CODIGO", "CONT_KEY", 1 "ALLOW_CONTAB_RES",'
        ' 1 "ALLOW_CONTAB_LIST",'
        ' "NAME", "%(fecha_inicio)s", "IP_ULL"'
        ' from "%(table)s" order by "NAME"')

    # one_entity_query gets one Convenio/Proyecto
    one_entity_query = (
        'select "CODIGO", "CONT_KEY", "IP_ULL",'
        ' "NAME", "%(fecha_inicio)s", 1 "ALLOW_CONTAB_RES",'
        ' 1 "ALLOW_CONTAB_LIST" from "%(table)s"'
        ' where "CODIGO"=\'%(entity)s\'')

    # user_categories_query gets the categories a user has (SigidiCategories).
    # These categories define what type of gestor the user is
    _dataids_from_dni_gestor = (
        'select "DATAID" from "OBJ_2274"'
        ' where "DNI"=\'{0}\' and "ISACTIVE"=1 and'
        ' (("VALID_FROM" is NULL or "VALID_FROM" < NOW())'
        ' and ("VALID_TO" is NULL or "VALID_TO" > NOW()))')

    _product_from_dataids = (
        'select "PROID" from "NIV_PRODUCTS"'
        ' where "PRODATAID" in (' + _dataids_from_dni_gestor + ')')

    user_categories_query = (
        'select "REL_PC_CATEGORYID" from "NIV_PROCATREL"'
        ' where "REL_PC_PRODUCTID" in (' + _product_from_dataids + ')')

    # entities_where_is_ip_query gets Proyectos/Convenios where the user is ip
    _refs_from_dataids = (
        'select "VRID" from "NIV_VALUES_REF"'
        ' where "VRTARGETDATAID" in (' + _dataid + ')')

    entities_where_is_ip_query = (
        'select "CODIGO", "CONT_KEY", "NAME", "IP_ULL", "%(fecha_inicio)s",'
        ' 1 "ALLOW_CONTAB_RES", 1 "ALLOW_CONTAB_LIST" from "%(table)s"'
        ' where "IP_ULL" in (' + _refs_from_dataids + ')')

    # The macroquery can be combined with any query that returns
    # Proyectos/Convenios (entities_where_is_ip_query, one_entity_query,
    # all_entities_query, permission_query)
    # It appends to the Proyectos/Convenios, the name of their IP.
    macroquery = (
        'select entities."CODIGO", entities."CONT_KEY",'
        ' "OBJ_2275"."NAME" "IP", entities."NAME",'
        ' entities."%(fecha_inicio)s" "DATE", entities."ALLOW_CONTAB_RES",'
        ' entities."ALLOW_CONTAB_LIST"'
        ' from "OBJ_2275" right join "NIV_VALUES_REF"'
        ' on "OBJ_2275"."DATAID" = "NIV_VALUES_REF"."VRTARGETDATAID"'
        ' right join (%(entities_query)s) entities'
        ' on "NIV_VALUES_REF"."VRID" = entities."IP_ULL"')


class SigidiConnection:

    _ent_tables = {SigidiEntityType.PROYECTOS: 'OBJ_2216',
                   SigidiEntityType.CONVENIOS: 'OBJ_2215'}

    _ent_dates = {SigidiEntityType.PROYECTOS: 'PROP_CONC_FECHA_ACEPT',
                  SigidiEntityType.CONVENIOS: 'FECHA_INICIO'}

    _proyectos_permissions = {
        SigidiCategories.SUPERUSUARIO,
        SigidiCategories.GESTOR_PROYECTOS,
        SigidiCategories.GESTOR_PROYECTOS_SOLO_LECTURA}

    _convenios_permissions = {
        SigidiCategories.SUPERUSUARIO,
        SigidiCategories.GESTOR_CONVENIOS_Y_CONTRATOS,
        SigidiCategories.GESTOR_CONVENIOS_Y_CONTRATOS_SOLO_LECTURA}

    def __init__(self, user=None):
        st.DATABASES['sigidi'] = st.SIGIDI_DB
        self.cursor = connections['sigidi'].cursor()
        self.cursor.__class__.make_query = _make_query
        self.cursor.__class__.make_query_dict = _make_query_dict
        self.user = user
        if user:
            self.cursor.execute(Sqry.vrid_query.format(user.profile.documento))
            user_permissions = self.cursor.fetchall()
            user_permissions = re.sub('[\[\]()]|,,', '',
                                      str(user_permissions)).strip(',')
            user_permissions = re.sub(',,', ',', user_permissions)
            if user_permissions == '':
                user_permissions = '0'
            self.user_permissions = user_permissions

    def _query_entity(self, permissions, entity_type):
        """Builds dynamically query to get projects for a user"""
        sentence = Sqry.permission_query
        for permission in permissions:
            sentence += Sqry.permission_query_end.format(
                permission.value, self.user_permissions) + " OR "
        sentence = sentence[:-4]  # Remove the last OR
        subquery = sentence % {'table': self._ent_tables[entity_type],
                               'fecha_inicio': self._ent_dates[entity_type]}
        return self._do_the_macroquery(subquery, self._ent_dates[entity_type])

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

    def _get_entity_where_has_permission(self, entity, entity_type):
        """
        Gets the specified project if the user has permission. If permission
        is not specified returns project where user has any permission
        """

        date_row = self._ent_dates[entity_type]

        if self._can_view_all_entities(entity_type):
            subquery = Sqry.one_entity_query % {
                'entity': entity, 'table': self._ent_tables[entity_type],
                'fecha_inicio': date_row}
            entities = self._do_the_macroquery(subquery, date_row)
            if entities:
                entity = entities[0]
                return entity
        permission = [SigidiPermissions.CONTAB_LIST,
                      SigidiPermissions.CONTAB_RES]

        # We ask to database for the projects that the user
        # has permissions for
        entities = self._query_entity(permission, entity_type)

        # We filter the project that was asked for
        for proj in entities:
            if proj['CODIGO'] == entity:
                return proj
        return False

    def _get_entities_where_is_ip(self, entity_type):
        date_row = self._ent_dates[entity_type]

        subquery = Sqry.entities_where_is_ip_query.format(
            self.user.profile.documento
        ) % {'table': self._ent_tables[entity_type], 'fecha_inicio': date_row}

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

    def _do_the_macroquery(self, subquery, date_format):
        return self.cursor.make_query_dict(Sqry.macroquery % {
            'entities_query': subquery,
            'fecha_inicio': date_format})

    def get_project(self, project_id):
        return self._get_entity(project_id, SigidiEntityType.PROYECTOS)

    def get_convenio(self, convenio_id):
        return self._get_entity(convenio_id, SigidiEntityType.CONVENIOS)

    def get_user_roles(self):
        roles = self.cursor.make_query(Sqry.user_categories_query.format(
            self.user.profile.documento))
        return set(self._codes_to_categories(roles))

    def can_view_all_projects(self):
        return self._has_any_role(self._proyectos_permissions)

    def can_view_all_convenios(self):
        return self._has_any_role(self._convenios_permissions)

    def get_all_projects(self):
        if self.user is None or self.can_view_all_projects():
            date_row = self._ent_dates[SigidiEntityType.PROYECTOS]
            entities_query = Sqry.all_entities_query % {
                'table': self._ent_tables[SigidiEntityType.PROYECTOS],
                'fecha_inicio': date_row}
            return self._do_the_macroquery(entities_query, date_row)
        return None

    def get_all_convenios(self):
        if self.user is None or self.can_view_all_convenios():
            date_row = self._ent_dates[SigidiEntityType.CONVENIOS]
            entities_query = Sqry.all_entities_query % {
                'table': self._ent_tables[SigidiEntityType.CONVENIOS],
                'fecha_inicio': date_row}
            return self._do_the_macroquery(entities_query, date_row)
        return None

    def get_user_projects(self):
        return self._get_user_entities(SigidiEntityType.PROYECTOS)

    def get_user_convenios(self):
        return self._get_user_entities(SigidiEntityType.CONVENIOS)

    def update_entities(self, entity_type):
        object_list = []
        entities = (self.get_all_convenios() if entity_type == Agreement
                    else self.get_all_projects())
        sigidi_entities = filter(lambda entity:
                                 entity['CODIGO'] is not None and
                                 entity['CONT_KEY'] is not None,
                                 entities)
        for entity in sigidi_entities:
            try:
                entity_type.objects.get(code=entity['CODIGO'])
            except ObjectDoesNotExist:
                new_entity = entity_type(code=entity['CODIGO'])
                if new_entity not in object_list:
                    object_list.append(new_entity)
        entity_type.objects.bulk_create(object_list)

    def update_projects(self):
        self.update_entities(Project)

    def update_agreements(self):
        self.update_entities(Agreement)
