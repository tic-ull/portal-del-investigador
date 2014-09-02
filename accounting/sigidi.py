# -*- encoding: UTF-8 -*-

from django.db import connections


class SigidiConnection:

    dataid = 'select "DATAID" from "OBJ_2275" where "DNI"=\'PASMEN2\''

    proid = 'select "PROID" from "NIV_PRODUCTS" where "PRODATAID"' \
            ' in (' + dataid + ')'

    vrid = 'select "VRID" from "NIV_VALUES_REF" where "VRTARGETID"' \
           ' in (' + proid + ')'

    codigo = 'select "CODIGO" from "OBJ_2216" where "ALLOW_CONTAB_RES"' \
             ' in (' + vrid + ')'

    def __init__(self):
        self.cursor = connections['sigidi'].cursor()

    def get_users(self):
        pass