# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
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


    def backwards(self, orm):
        # Deleting model 'Articulo'
        db.delete_table(u'cvn_articulo')

        # Deleting model 'Libro'
        db.delete_table(u'cvn_libro')

        # Deleting model 'Capitulo'
        db.delete_table(u'cvn_capitulo')


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
        u'cvn.produccion': {
            'Meta': {'object_name': 'Produccion'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indice_h': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cvn.Usuario']"})
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
        u'cvn.situacionprofesional': {
            'Meta': {'object_name': 'SituacionProfesional'},
            'categoria_or_puesto': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'ciudad_de_trabajo': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'comunidad_or_region_trabajo': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'correo_electronico': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dedicacion_profesional': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'departamento_or_servicio': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'docente': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'duracion_anyos': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'duracion_dias': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'duracion_meses': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'especializacion_primaria': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'especializacion_secundaria': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'especializacion_terciaria': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'facultad_or_escuela': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'fecha_de_fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_de_inicio': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interes_doc_investigacion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'modalidad_del_contrato': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'nombre_de_la_entidad': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'pais_de_trabajo': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'palabras_clave_dedicacion': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'telefono_fax_cod': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'telefono_fax_ext': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'telefono_fax_num': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'telefono_fijo_cod': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'telefono_fijo_ext': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'telefono_fijo_num': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tipo_de_actividad_de_gestion': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'tipo_de_dedicacion': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'tipo_de_entidad': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cvn.Usuario']"})
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