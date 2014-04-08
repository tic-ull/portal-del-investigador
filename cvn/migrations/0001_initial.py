# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CVN'
        db.create_table(u'cvn_cvn', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cvn_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('xml_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('fecha_cvn', self.gf('django.db.models.fields.DateField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'cvn', ['CVN'])

        # Adding model 'UserProfile'
        db.create_table(u'cvn_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('cvn', self.gf('django.db.models.fields.related.OneToOneField')(related_name='user_profile', null=True, on_delete=models.SET_NULL, to=orm['cvn.CVN'], blank=True, unique=True)),
            ('documento', self.gf('django.db.models.fields.CharField')(max_length=20, unique=True, null=True, blank=True)),
            ('rrhh_code', self.gf('django.db.models.fields.CharField')(max_length=20, unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'cvn', ['UserProfile'])

        # Adding model 'Publicacion'
        db.create_table(u'cvn_publicacion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('tipo_de_produccion', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('fecha', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('tipo_de_soporte', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('nombre_publicacion', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('editorial', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('volumen', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('numero', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('pagina_inicial', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('pagina_final', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('autores', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('posicion_sobre_total', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('en_calidad_de', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('issn', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('deposito_legal', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=500, null=True, blank=True)),
            ('coleccion', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('ciudad', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('pais', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('comunidad_or_region', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('fuente_de_impacto', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('categoria', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('indice_de_impacto', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('posicion', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('num_revistas', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('revista_25', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('fuente_de_citas', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('citas', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('publicacion_relevante', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('resenyas_en_revista', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('filtro', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('resultados_destacados', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'cvn', ['Publicacion'])

        # Adding M2M table for field user_profile on 'Publicacion'
        m2m_table_name = db.shorten_name(u'cvn_publicacion_user_profile')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('publicacion', models.ForeignKey(orm[u'cvn.publicacion'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'cvn.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['publicacion_id', 'userprofile_id'])

        # Adding model 'Articulo'
        db.create_table(u'cvn_articulo', (
            (u'publicacion_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cvn.Publicacion'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'cvn', ['Articulo'])

        # Adding model 'Libro'
        db.create_table(u'cvn_libro', (
            (u'publicacion_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cvn.Publicacion'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'cvn', ['Libro'])

        # Adding model 'Capitulo'
        db.create_table(u'cvn_capitulo', (
            (u'publicacion_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cvn.Publicacion'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'cvn', ['Capitulo'])

        # Adding model 'Congreso'
        db.create_table(u'cvn_congreso', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('fecha_realizacion', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('fecha_finalizacion', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('nombre_del_congreso', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('ciudad_de_realizacion', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('pais_de_realizacion', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('comunidad_or_region_realizacion', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('entidad_organizadora', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ciudad', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('autores', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('titulo_publicacion', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('tipo_evento', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('fecha', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('nombre_de_publicacion', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('comite_admision_externa', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('ambito', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('otro_ambito', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('tipo_de_participacion', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('intervencion_por', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('volumen', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('numero', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('pagina_inicial', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('pagina_final', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('editorial', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('issn', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('deposito_legal', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('publicacion_acta_congreso', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=500, null=True, blank=True)),
            ('pais', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('comunidad_or_region', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'cvn', ['Congreso'])

        # Adding M2M table for field user_profile on 'Congreso'
        m2m_table_name = db.shorten_name(u'cvn_congreso_user_profile')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('congreso', models.ForeignKey(orm[u'cvn.congreso'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'cvn.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['congreso_id', 'userprofile_id'])

        # Adding model 'Proyecto'
        db.create_table(u'cvn_proyecto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('denominacion_del_proyecto', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('numero_de_investigadores', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('autores', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('entidad_de_realizacion', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('ciudad_del_proyecto', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('pais_del_proyecto', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('comunidad_or_region_proyecto', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('entidad_financiadora', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('tipo_de_entidad', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('ciudad_de_la_entidad', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('pais_de_la_entidad', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('comunidad_or_region_entidad', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('fecha_de_inicio', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('fecha_de_fin', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('cuantia_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=19, decimal_places=2, blank=True)),
            ('duracion_anyos', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('duracion_meses', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('duracion_dias', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('palabras_clave', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('modalidad_del_proyecto', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('ambito', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('otro_ambito', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('numero_personas_anyo', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('calidad_participacion', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('tipo_participacion', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('nombre_del_programa', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('cod_segun_financiadora', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('cuantia_subproyecto', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=19, decimal_places=2, blank=True)),
            ('porcentaje_en_subvencion', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=19, decimal_places=2, blank=True)),
            ('porcentaje_en_credito', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=19, decimal_places=2, blank=True)),
            ('porcentaje_mixto', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=19, decimal_places=2, blank=True)),
            ('resultados_mas_relevantes', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('dedicacion', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('palabras_clave_dedicacion', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('entidad_participante', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('aportacion_del_solicitante', self.gf('django.db.models.fields.TextField')(max_length=2048, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'cvn', ['Proyecto'])

        # Adding M2M table for field user_profile on 'Proyecto'
        m2m_table_name = db.shorten_name(u'cvn_proyecto_user_profile')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('proyecto', models.ForeignKey(orm[u'cvn.proyecto'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'cvn.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['proyecto_id', 'userprofile_id'])

        # Adding model 'Convenio'
        db.create_table(u'cvn_convenio', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('denominacion_del_proyecto', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('numero_de_investigadores', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('autores', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('entidad_financiadora', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('tipo_de_entidad', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('ciudad_de_la_entidad', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('pais_de_la_entidad', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('comunidad_or_region_entidad', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('calidad_participacion', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('entidad_participante', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('fecha_de_inicio', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('duracion_anyos', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('duracion_meses', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('duracion_dias', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cuantia_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=19, decimal_places=2, blank=True)),
            ('modalidad_del_proyecto', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('ambito', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('otro_ambito', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('entidad_de_realizacion', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('ciudad_del_proyecto', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('pais_del_proyecto', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('comunidad_or_region_proyecto', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('numero_personas_anyo', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('tipo_proyecto', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('nombre_del_programa', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
            ('cod_segun_financiadora', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('cuantia_subproyecto', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=19, decimal_places=2, blank=True)),
            ('porcentaje_en_subvencion', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=19, decimal_places=2, blank=True)),
            ('porcentaje_en_credito', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=19, decimal_places=2, blank=True)),
            ('porcentaje_mixto', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=19, decimal_places=2, blank=True)),
            ('resultados_mas_relevantes', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('palabras_clave', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'cvn', ['Convenio'])

        # Adding M2M table for field user_profile on 'Convenio'
        m2m_table_name = db.shorten_name(u'cvn_convenio_user_profile')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('convenio', models.ForeignKey(orm[u'cvn.convenio'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'cvn.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['convenio_id', 'userprofile_id'])

        # Adding model 'TesisDoctoral'
        db.create_table(u'cvn_tesisdoctoral', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('fecha_de_lectura', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('autor', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('universidad_que_titula', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('ciudad_del_trabajo', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('pais_del_trabajo', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('comunidad_or_region_trabajo', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('tipo_de_proyecto', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('codirector', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('calificacion', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('mencion_de_calidad', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('fecha_mencion_de_calidad', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('doctorado_europeo', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('fecha_mencion_doctorado_europeo', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('palabras_clave_titulo', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'cvn', ['TesisDoctoral'])

        # Adding M2M table for field user_profile on 'TesisDoctoral'
        m2m_table_name = db.shorten_name(u'cvn_tesisdoctoral_user_profile')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tesisdoctoral', models.ForeignKey(orm[u'cvn.tesisdoctoral'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'cvn.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tesisdoctoral_id', 'userprofile_id'])


    def backwards(self, orm):
        # Deleting model 'CVN'
        db.delete_table(u'cvn_cvn')

        # Deleting model 'UserProfile'
        db.delete_table(u'cvn_userprofile')

        # Deleting model 'Publicacion'
        db.delete_table(u'cvn_publicacion')

        # Removing M2M table for field user_profile on 'Publicacion'
        db.delete_table(db.shorten_name(u'cvn_publicacion_user_profile'))

        # Deleting model 'Articulo'
        db.delete_table(u'cvn_articulo')

        # Deleting model 'Libro'
        db.delete_table(u'cvn_libro')

        # Deleting model 'Capitulo'
        db.delete_table(u'cvn_capitulo')

        # Deleting model 'Congreso'
        db.delete_table(u'cvn_congreso')

        # Removing M2M table for field user_profile on 'Congreso'
        db.delete_table(db.shorten_name(u'cvn_congreso_user_profile'))

        # Deleting model 'Proyecto'
        db.delete_table(u'cvn_proyecto')

        # Removing M2M table for field user_profile on 'Proyecto'
        db.delete_table(db.shorten_name(u'cvn_proyecto_user_profile'))

        # Deleting model 'Convenio'
        db.delete_table(u'cvn_convenio')

        # Removing M2M table for field user_profile on 'Convenio'
        db.delete_table(db.shorten_name(u'cvn_convenio_user_profile'))

        # Deleting model 'TesisDoctoral'
        db.delete_table(u'cvn_tesisdoctoral')

        # Removing M2M table for field user_profile on 'TesisDoctoral'
        db.delete_table(db.shorten_name(u'cvn_tesisdoctoral_user_profile'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'cvn.articulo': {
            'Meta': {'ordering': "['-fecha', 'titulo']", 'object_name': 'Articulo', '_ormbases': [u'cvn.Publicacion']},
            u'publicacion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['cvn.Publicacion']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'cvn.capitulo': {
            'Meta': {'ordering': "['-fecha', 'titulo']", 'object_name': 'Capitulo', '_ormbases': [u'cvn.Publicacion']},
            u'publicacion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['cvn.Publicacion']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'cvn.congreso': {
            'Meta': {'ordering': "['-fecha_realizacion', 'titulo']", 'object_name': 'Congreso'},
            'ambito': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'autores': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ciudad': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'ciudad_de_realizacion': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'comite_admision_externa': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'comunidad_or_region': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'comunidad_or_region_realizacion': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deposito_legal': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'editorial': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'entidad_organizadora': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_finalizacion': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_realizacion': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intervencion_por': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'issn': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'nombre_de_publicacion': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'nombre_del_congreso': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'numero': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'otro_ambito': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'pagina_final': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pagina_inicial': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pais': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'pais_de_realizacion': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'publicacion_acta_congreso': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'tipo_de_participacion': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'tipo_evento': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'titulo_publicacion': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'user_profile': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['cvn.UserProfile']", 'null': 'True', 'blank': 'True'}),
            'volumen': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'cvn.convenio': {
            'Meta': {'ordering': "['-fecha_de_inicio', 'denominacion_del_proyecto']", 'object_name': 'Convenio'},
            'ambito': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'autores': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'calidad_participacion': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'ciudad_de_la_entidad': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'ciudad_del_proyecto': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'cod_segun_financiadora': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'comunidad_or_region_entidad': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'comunidad_or_region_proyecto': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cuantia_subproyecto': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '2', 'blank': 'True'}),
            'cuantia_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '2', 'blank': 'True'}),
            'denominacion_del_proyecto': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'duracion_anyos': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'duracion_dias': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'duracion_meses': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'entidad_de_realizacion': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'entidad_financiadora': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'entidad_participante': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'fecha_de_inicio': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modalidad_del_proyecto': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'nombre_del_programa': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'numero_de_investigadores': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'numero_personas_anyo': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'otro_ambito': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'pais_de_la_entidad': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'pais_del_proyecto': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'palabras_clave': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'porcentaje_en_credito': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '2', 'blank': 'True'}),
            'porcentaje_en_subvencion': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '2', 'blank': 'True'}),
            'porcentaje_mixto': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '2', 'blank': 'True'}),
            'resultados_mas_relevantes': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'tipo_de_entidad': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'tipo_proyecto': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_profile': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['cvn.UserProfile']", 'null': 'True', 'blank': 'True'})
        },
        u'cvn.cvn': {
            'Meta': {'object_name': 'CVN'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cvn_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'fecha_cvn': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'xml_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'cvn.fecyt': {
            'Meta': {'object_name': 'FECYT', 'managed': 'False'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cvn.libro': {
            'Meta': {'ordering': "['-fecha', 'titulo']", 'object_name': 'Libro', '_ormbases': [u'cvn.Publicacion']},
            u'publicacion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['cvn.Publicacion']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'cvn.proyecto': {
            'Meta': {'ordering': "['-fecha_de_inicio', 'denominacion_del_proyecto']", 'object_name': 'Proyecto'},
            'ambito': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'aportacion_del_solicitante': ('django.db.models.fields.TextField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'autores': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'calidad_participacion': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'ciudad_de_la_entidad': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'ciudad_del_proyecto': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'cod_segun_financiadora': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'comunidad_or_region_entidad': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'comunidad_or_region_proyecto': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cuantia_subproyecto': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '2', 'blank': 'True'}),
            'cuantia_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '2', 'blank': 'True'}),
            'dedicacion': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'denominacion_del_proyecto': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'duracion_anyos': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'duracion_dias': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'duracion_meses': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'entidad_de_realizacion': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'entidad_financiadora': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'entidad_participante': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'fecha_de_fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_de_inicio': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modalidad_del_proyecto': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'nombre_del_programa': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'numero_de_investigadores': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'numero_personas_anyo': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'otro_ambito': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'pais_de_la_entidad': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'pais_del_proyecto': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'palabras_clave': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'palabras_clave_dedicacion': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'porcentaje_en_credito': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '2', 'blank': 'True'}),
            'porcentaje_en_subvencion': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '2', 'blank': 'True'}),
            'porcentaje_mixto': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '2', 'blank': 'True'}),
            'resultados_mas_relevantes': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'tipo_de_entidad': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'tipo_participacion': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_profile': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['cvn.UserProfile']", 'null': 'True', 'blank': 'True'})
        },
        u'cvn.publicacion': {
            'Meta': {'ordering': "['-fecha', 'titulo']", 'object_name': 'Publicacion'},
            'autores': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'categoria': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'citas': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'ciudad': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'coleccion': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'comunidad_or_region': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deposito_legal': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'editorial': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'en_calidad_de': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'filtro': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'fuente_de_citas': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'fuente_de_impacto': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indice_de_impacto': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'issn': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'nombre_publicacion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'num_revistas': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'numero': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pagina_final': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pagina_inicial': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pais': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'posicion': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'posicion_sobre_total': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'publicacion_relevante': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'resenyas_en_revista': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'resultados_destacados': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'revista_25': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tipo_de_produccion': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tipo_de_soporte': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'user_profile': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['cvn.UserProfile']", 'null': 'True', 'blank': 'True'}),
            'volumen': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'cvn.tesisdoctoral': {
            'Meta': {'ordering': "['-fecha_de_lectura', 'titulo']", 'object_name': 'TesisDoctoral'},
            'autor': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'calificacion': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ciudad_del_trabajo': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'codirector': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'comunidad_or_region_trabajo': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'doctorado_europeo': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'fecha_de_lectura': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_mencion_de_calidad': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_mencion_doctorado_europeo': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mencion_de_calidad': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'pais_del_trabajo': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'palabras_clave_titulo': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'tipo_de_proyecto': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'universidad_que_titula': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_profile': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['cvn.UserProfile']", 'null': 'True', 'blank': 'True'})
        },
        u'cvn.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'cvn': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'user_profile'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['cvn.CVN']", 'blank': 'True', 'unique': 'True'}),
            'documento': ('django.db.models.fields.CharField', [], {'max_length': '20', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rrhh_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['cvn']