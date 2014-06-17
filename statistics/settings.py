# -*- encoding: UTF-8 -*-

from django.conf import settings as st


WS_ALL_DEPARTMENTS = st.WS_SERVER_URL + 'get_departamentos_y_miembros'
WS_DEPARTMENT = (st.WS_SERVER_URL +
                 'get_departamento_y_miembros?cod_departamento=%s')
WS_DEPARTMENT_YEAR = st.WS_SERVER_URL + 'get_departamentos?ano=%s'
WS_DEPARTMENT_INFO = (st.WS_SERVER_URL +
                      'get_info_departamento?cod_departamento=%s')
WS_INFO_USER = st.WS_SERVER_URL + 'get_departamento_y_miembros?cod_persona=%s'
WS_INFO_PDI = st.WS_SERVER_URL + 'get_info_pdi?cod_persona=%s'
WS_INFO_PDI_YEAR = st.WS_SERVER_URL + 'get_info_pdi?cod_persona=%s&ano=%s'
WS_PDI_VALID = st.WS_SERVER_URL + 'get_pdi_vigente?cod_%s=%s&ano=%s'
# WS_CATEGORY = st.WS_SERVER_URL +'get_cce'
WS_CATEGORY = st.WS_SERVER_URL + 'get_cce?past_days=%s'

PERCENT_VALID_DEPT_CVN = 75
