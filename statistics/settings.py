# -*- encoding: UTF-8 -*-

from django.conf import settings as st


WS_ALL_DEPARTMETS = st.WS_SERVER_URL + 'get_departamentos_y_miembros'
WS_DEPARTMEMT = (st.WS_SERVER_URL +
                 'get_departamento_y_miembros?cod_departamento=%s')
WS_INFO_PDI = st.WS_SERVER_URL + 'get_info_pdi?cod_persona=%s'

PERCENT_VALID_DEPT_CVN = 75

PROFESSIONAL_CATEGORY = [5609, 5610, 5611, 5612, 5617, 5632, 5686, 5687, 5709,
                         5710, 5711, 5712, 5826, 5827, 5828, 5913, 5944, 5955,
                         5989, 5990, 5991, 5992, 5993, 5994, 5995, 5996, 5997,
                         5998, 5999, 6001, 6002, 6004, 6005, 6007, 6288, 6289,
                         6291, 6292, 6643, 6646, 6663, 6700, 6718, 7335]
