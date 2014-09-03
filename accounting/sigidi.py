from django.db import connections
from django.contrib.auth.models import User
import re

class SigidiPermissions:
    CONTAB_RES = "ALLOW_CONTAB_RES"
    CONTAB_LIST = "ALLOW_CONTAB_LIST"

class SigidiUserPermissions:

    dataid = 'select "DATAID" from "OBJ_2275" where "DNI"=\'{0}\''

    proid = 'select "PROID" from "NIV_PRODUCTS" where "PRODATAID"' \
            ' in (' + dataid + ')'

    vrid = 'select "VRID" from "NIV_VALUES_REF" where "VRTARGETID"' \
           ' in (' + proid + ')'

    permission_query = 'select "CODIGO" from "OBJ_2216" where "{0}"' \
                       ' in ({1})'

    def __init__(self, user):
        self.cursor = connections['sigidi'].cursor()
        user = User.objects.get(profile__documento='PASMEN2')
        self.cursor.execute(self.vrid.format(user.profile.documento))
        user_permissions = self.cursor.fetchall()
        user_permissions = re.sub('[\[\]()]|,,', '',
                                       str(user_permissions)).strip(',')
        self.user_permissions = re.sub(',,', ',', user_permissions)

    def has_perm(self, permission, project):
        self.cursor.execute(self.permission_query.format(permission,
                                                         self.user_permissions))
        projects = self.cursor.fetchall()
        for proj in projects:
            if proj[0] == project:
                return True
        return False


    def can_contab_res(self, project):
        return self.has_perm(SigidiPermissions.CONTAB_RES, project)

    def can_contab_list(self, project):
        return self.has_perm(SigidiPermissions.CONTAB_LIST)