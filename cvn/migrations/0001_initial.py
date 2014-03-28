# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Usuario'
        db.create_table(u'cvn_usuario', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('primer_apellido', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('segundo_apellido', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('sexo', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('fecha_nacimiento', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('tipo_documento', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('correo_electronico', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('documento', self.gf('django.db.models.fields.CharField')(max_length=20, unique=True, null=True, blank=True)),
            ('telefono_fijo_cod', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('telefono_fijo_num', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('telefono_fijo_ext', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('telefono_fax_cod', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('telefono_fax_num', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('telefono_fax_ext', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('telefono_movil_cod', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('telefono_movil_num', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('telefono_movil_ext', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('imagen', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('pagina_web_personal', self.gf('django.db.models.fields.URLField')(max_length=128, null=True, blank=True)),
            ('direccion', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('resto_direccion', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('codigo_postal', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('ciudad_de_contacto', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('pais_de_contacto', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('comunidad', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('provincia', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('nacionalidad', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('ciudad_de_nacimiento', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('pais_de_nacimiento', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('comunidad_nacimiento', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'cvn', ['Usuario'])

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

        # Adding M2M table for field usuario on 'Publicacion'
        m2m_table_name = db.shorten_name(u'cvn_publicacion_usuario')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('publicacion', models.ForeignKey(orm[u'cvn.publicacion'], null=False)),
            ('usuario', models.ForeignKey(orm[u'cvn.usuario'], null=False))
        ))
        db.create_unique(m2m_table_name, ['publicacion_id', 'usuario_id'])

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

        # Adding M2M table for field usuario on 'Congreso'
        m2m_table_name = db.shorten_name(u'cvn_congreso_usuario')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('congreso', models.ForeignKey(orm[u'cvn.congreso'], null=False)),
            ('usuario', models.ForeignKey(orm[u'cvn.usuario'], null=False))
        ))
        db.create_unique(m2m_table_name, ['congreso_id', 'usuario_id'])

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

        # Adding M2M table for field usuario on 'Proyecto'
        m2m_table_name = db.shorten_name(u'cvn_proyecto_usuario')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('proyecto', models.ForeignKey(orm[u'cvn.proyecto'], null=False)),
            ('usuario', models.ForeignKey(orm[u'cvn.usuario'], null=False))
        ))
        db.create_unique(m2m_table_name, ['proyecto_id', 'usuario_id'])

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

        # Adding M2M table for field usuario on 'Convenio'
        m2m_table_name = db.shorten_name(u'cvn_convenio_usuario')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('convenio', models.ForeignKey(orm[u'cvn.convenio'], null=False)),
            ('usuario', models.ForeignKey(orm[u'cvn.usuario'], null=False))
        ))
        db.create_unique(m2m_table_name, ['convenio_id', 'usuario_id'])

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

        # Adding M2M table for field usuario on 'TesisDoctoral'
        m2m_table_name = db.shorten_name(u'cvn_tesisdoctoral_usuario')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tesisdoctoral', models.ForeignKey(orm[u'cvn.tesisdoctoral'], null=False)),
            ('usuario', models.ForeignKey(orm[u'cvn.usuario'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tesisdoctoral_id', 'usuario_id'])


    def backwards(self, orm):
        # Deleting model 'Usuario'
        db.delete_table(u'cvn_usuario')

        # Deleting model 'Publicacion'
        db.delete_table(u'cvn_publicacion')

        # Removing M2M table for field usuario on 'Publicacion'
        db.delete_table(db.shorten_name(u'cvn_publicacion_usuario'))

        # Deleting model 'Articulo'
        db.delete_table(u'cvn_articulo')

        # Deleting model 'Libro'
        db.delete_table(u'cvn_libro')

        # Deleting model 'Capitulo'
        db.delete_table(u'cvn_capitulo')

        # Deleting model 'Congreso'
        db.delete_table(u'cvn_congreso')

        # Removing M2M table for field usuario on 'Congreso'
        db.delete_table(db.shorten_name(u'cvn_congreso_usuario'))

        # Deleting model 'Proyecto'
        db.delete_table(u'cvn_proyecto')

        # Removing M2M table for field usuario on 'Proyecto'
        db.delete_table(db.shorten_name(u'cvn_proyecto_usuario'))

        # Deleting model 'Convenio'
        db.delete_table(u'cvn_convenio')

        # Removing M2M table for field usuario on 'Convenio'
        db.delete_table(db.shorten_name(u'cvn_convenio_usuario'))

        # Deleting model 'TesisDoctoral'
        db.delete_table(u'cvn_tesisdoctoral')

        # Removing M2M table for field usuario on 'TesisDoctoral'
        db.delete_table(db.shorten_name(u'cvn_tesisdoctoral_usuario'))


    models = {
        u'cvn.articulo': {
            'Meta': {'object_name': 'Articulo', '_ormbases': [u'cvn.Publicacion']},
            u'publicacion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['cvn.Publicacion']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'cvn.capitulo': {
            'Meta': {'object_name': 'Capitulo', '_ormbases': [u'cvn.Publicacion']},
            u'publicacion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['cvn.Publicacion']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'cvn.congreso': {
            'Meta': {'object_name': 'Congreso'},
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
            'usuario': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['cvn.Usuario']", 'null': 'True', 'blank': 'True'}),
            'volumen': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'cvn.convenio': {
            'Meta': {'object_name': 'Convenio'},
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
            'usuario': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['cvn.Usuario']", 'null': 'True', 'blank': 'True'})
        },
        u'cvn.libro': {
            'Meta': {'object_name': 'Libro', '_ormbases': [u'cvn.Publicacion']},
            u'publicacion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['cvn.Publicacion']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'cvn.proyecto': {
            'Meta': {'object_name': 'Proyecto'},
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
            'usuario': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['cvn.Usuario']", 'null': 'True', 'blank': 'True'})
        },
        u'cvn.publicacion': {
            'Meta': {'object_name': 'Publicacion'},
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
            'usuario': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['cvn.Usuario']", 'null': 'True', 'blank': 'True'}),
            'volumen': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'cvn.tesisdoctoral': {
            'Meta': {'object_name': 'TesisDoctoral'},
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
            'usuario': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['cvn.Usuario']", 'null': 'True', 'blank': 'True'})
        },
        u'cvn.usuario': {
            'Meta': {'object_name': 'Usuario'},
            'ciudad_de_contacto': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'ciudad_de_nacimiento': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'codigo_postal': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'comunidad': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'comunidad_nacimiento': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'correo_electronico': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'documento': ('django.db.models.fields.CharField', [], {'max_length': '20', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'fecha_nacimiento': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nacionalidad': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'pagina_web_personal': ('django.db.models.fields.URLField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'pais_de_contacto': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'pais_de_nacimiento': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'primer_apellido': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'provincia': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'resto_direccion': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'segundo_apellido': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sexo': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'telefono_fax_cod': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'telefono_fax_ext': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'telefono_fax_num': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'telefono_fijo_cod': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'telefono_fijo_ext': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'telefono_fijo_num': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'telefono_movil_cod': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'telefono_movil_ext': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'telefono_movil_num': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'tipo_documento': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cvn']