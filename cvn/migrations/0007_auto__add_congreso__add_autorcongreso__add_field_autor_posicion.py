# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Congreso'
        db.create_table(u'cvn_congreso', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cvn.Usuario'])),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('fecha_realizacion', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('fecha_finalizacion', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('nombre_del_congreso', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('ciudad_de_realizacion', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('pais_de_realizacion', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('comunidad_or_region_realizacion', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('entidad_organizadora', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('ciudad', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('titulo_publicacion', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('tipo_evento', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('fecha', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('nombre_de_publicacion', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('comite_admision_externa', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('ambito_del_congreso', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('tipo_de_participacion', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('intervencion_por', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('volumen', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('numero', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('pagina_inicial', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('pagina_final', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('editorial', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('issn', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('deposito_legal', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('publicacion_acta_congreso', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=128, null=True, blank=True)),
            ('pais', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('comunidad_or_region', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'cvn', ['Congreso'])

        # Adding model 'AutorCongreso'
        db.create_table(u'cvn_autorcongreso', (
            (u'autor_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cvn.Autor'], unique=True, primary_key=True)),
            ('congreso', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cvn.Congreso'])),
        ))
        db.send_create_signal(u'cvn', ['AutorCongreso'])

        # Adding field 'Autor.posicion'
        db.add_column(u'cvn_autor', 'posicion',
                      self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Congreso'
        db.delete_table(u'cvn_congreso')

        # Deleting model 'AutorCongreso'
        db.delete_table(u'cvn_autorcongreso')

        # Deleting field 'Autor.posicion'
        db.delete_column(u'cvn_autor', 'posicion')


    models = {
        u'cvn.autor': {
            'Meta': {'object_name': 'Autor'},
            'firma': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'posicion': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'primer_apellido': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'segundo_apellido': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'cvn.autorcongreso': {
            'Meta': {'object_name': 'AutorCongreso', '_ormbases': [u'cvn.Autor']},
            u'autor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['cvn.Autor']", 'unique': 'True', 'primary_key': 'True'}),
            'congreso': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cvn.Congreso']"})
        },
        u'cvn.autorpublicacion': {
            'Meta': {'object_name': 'AutorPublicacion', '_ormbases': [u'cvn.Autor']},
            u'autor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['cvn.Autor']", 'unique': 'True', 'primary_key': 'True'}),
            'publicacion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cvn.Publicacion']"})
        },
        u'cvn.congreso': {
            'Meta': {'object_name': 'Congreso'},
            'ambito_del_congreso': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'ciudad': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'ciudad_de_realizacion': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'comite_admision_externa': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'comunidad_or_region': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'comunidad_or_region_realizacion': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deposito_legal': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'editorial': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'entidad_organizadora': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_finalizacion': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_realizacion': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intervencion_por': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'issn': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'nombre_de_publicacion': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'nombre_del_congreso': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'numero': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'pagina_final': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'pagina_inicial': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'pais': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'pais_de_realizacion': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'publicacion_acta_congreso': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tipo_de_participacion': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'tipo_evento': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'titulo_publicacion': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cvn.Usuario']"}),
            'volumen': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
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
        u'cvn.publicacion': {
            'Meta': {'object_name': 'Publicacion'},
            'categoria': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'citas': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'ciudad': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'coleccion': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'comunidad_or_region': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deposito_legal': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'editorial': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'en_calidad_de': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'filtro': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'fuente_de_citas': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'fuente_de_impacto': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indice_de_impacto': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'issn': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'nombre_publicacion': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'num_revistas_catoria': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'numero': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'pagina_final': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'pagina_inicial': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'pais': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'posicion': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'posicion_sobre_total': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'publicacion_relevante': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'resenyas_en_revista': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'resultados_destacados': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'revista_25': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'tipo_de_produccion': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tipo_de_soporte': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'titulo_publicacion': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cvn.Usuario']"}),
            'volumen': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
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
            'documento': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'fecha_nacimiento': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'investigador': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['viinvDB.GrupoinvestInvestigador']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
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
        },
        u'viinvDB.authuser': {
            'Meta': {'object_name': 'AuthUser', 'db_table': "u'auth_user'"},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '75L'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30L'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.IntegerField', [], {}),
            'is_staff': ('django.db.models.fields.IntegerField', [], {}),
            'is_superuser': ('django.db.models.fields.IntegerField', [], {}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30L'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128L'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30L'})
        },
        u'viinvDB.grupoinvestareaconocimiento': {
            'Meta': {'object_name': 'GrupoinvestAreaconocimiento', 'db_table': "u'GrupoInvest_areaconocimiento'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100L'})
        },
        u'viinvDB.grupoinvestareainvestigacionanep': {
            'Meta': {'object_name': 'GrupoinvestAreainvestigacionanep', 'db_table': "u'GrupoInvest_areainvestigacionanep'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100L'})
        },
        u'viinvDB.grupoinvestareasinvestigacion': {
            'Meta': {'object_name': 'GrupoinvestAreasinvestigacion', 'db_table': "u'GrupoInvest_areasinvestigacion'"},
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '60L'})
        },
        u'viinvDB.grupoinvestcategoriainvestigador': {
            'Meta': {'object_name': 'GrupoinvestCategoriainvestigador', 'db_table': "u'GrupoInvest_categoriainvestigador'"},
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '40L'})
        },
        u'viinvDB.grupoinvestcentro': {
            'Meta': {'object_name': 'GrupoinvestCentro', 'db_table': "u'GrupoInvest_centro'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100L'})
        },
        u'viinvDB.grupoinvestdepartamento': {
            'Meta': {'object_name': 'GrupoinvestDepartamento', 'db_table': "u'GrupoInvest_departamento'"},
            'codigo': ('django.db.models.fields.CharField', [], {'max_length': '5L'}),
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '120L'})
        },
        u'viinvDB.grupoinvestgrupoinves': {
            'Meta': {'object_name': 'GrupoinvestGrupoinves', 'db_table': "u'GrupoInvest_grupoinves'"},
            'acronimo': ('django.db.models.fields.CharField', [], {'max_length': '20L', 'blank': 'True'}),
            'activo': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['viinvDB.GrupoinvestAreasinvestigacion']", 'null': 'True', 'blank': 'True'}),
            'area_anep': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'anep_to_anep_inves'", 'null': 'True', 'to': u"orm['viinvDB.GrupoinvestAreainvestigacionanep']"}),
            'area_anep2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'anep_to_anep2_inves'", 'null': 'True', 'to': u"orm['viinvDB.GrupoinvestAreainvestigacionanep']"}),
            'area_anep3': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'anep_to_anep3_inves'", 'null': 'True', 'to': u"orm['viinvDB.GrupoinvestAreainvestigacionanep']"}),
            'centro': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['viinvDB.GrupoinvestCentro']", 'null': 'True', 'blank': 'True'}),
            'coordinador': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['viinvDB.GrupoinvestInvestigador']", 'null': 'True', 'blank': 'True'}),
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['viinvDB.GrupoinvestDepartamento']", 'null': 'True', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'direccion': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '75L', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20L', 'blank': 'True'}),
            'grupo': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'instituto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['viinvDB.GrupoinvestInstituto']", 'null': 'True', 'blank': 'True'}),
            'subarea': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['viinvDB.GrupoinvestSubareasinvestigacion']", 'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '255L'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '20L', 'blank': 'True'}),
            'web': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'blank': 'True'})
        },
        u'viinvDB.grupoinvestinstituto': {
            'Meta': {'object_name': 'GrupoinvestInstituto', 'db_table': "u'GrupoInvest_instituto'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100L'})
        },
        u'viinvDB.grupoinvestinvestigador': {
            'Meta': {'object_name': 'GrupoinvestInvestigador', 'db_table': "u'GrupoInvest_investigador'"},
            'apellido1': ('django.db.models.fields.CharField', [], {'max_length': '60L'}),
            'apellido2': ('django.db.models.fields.CharField', [], {'max_length': '60L'}),
            'area_anep': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'anep_to_anep'", 'null': 'True', 'to': u"orm['viinvDB.GrupoinvestAreainvestigacionanep']"}),
            'area_anep2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'anep_to_anep2'", 'null': 'True', 'to': u"orm['viinvDB.GrupoinvestAreainvestigacionanep']"}),
            'area_anep3': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'anep_to_anep3'", 'null': 'True', 'to': u"orm['viinvDB.GrupoinvestAreainvestigacionanep']"}),
            'areaconocimiento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['viinvDB.GrupoinvestAreaconocimiento']", 'null': 'True', 'db_column': "u'areaConocimiento_id'", 'blank': 'True'}),
            'cas_username': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'blank': 'True'}),
            'categoria': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['viinvDB.GrupoinvestCategoriainvestigador']"}),
            'centro': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['viinvDB.GrupoinvestCentro']", 'null': 'True', 'blank': 'True'}),
            'cese': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cod_persona': ('django.db.models.fields.CharField', [], {'max_length': '5L'}),
            'confirma_grupo_a': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'confirma_grupo_A'", 'blank': 'True'}),
            'confirma_grupo_b': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'confirma_grupo_B'", 'blank': 'True'}),
            'dedicacion': ('django.db.models.fields.CharField', [], {'max_length': '8L'}),
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['viinvDB.GrupoinvestDepartamento']", 'null': 'True', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '60L'}),
            'fecha_nacimiento': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'blank': 'True'}),
            'fin_sexenio': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'grupo_a': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'Perteneciente(A)'", 'null': 'True', 'db_column': "u'grupo_A_id'", 'to': u"orm['viinvDB.GrupoinvestGrupoinves']"}),
            'grupo_activo': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'Perteneciente'", 'null': 'True', 'to': u"orm['viinvDB.GrupoinvestGrupoinves']"}),
            'grupo_b': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'Perteneciente(B)'", 'null': 'True', 'db_column': "u'grupo_B_id'", 'to': u"orm['viinvDB.GrupoinvestGrupoinves']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'inicio_sexenio': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'instituto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['viinvDB.GrupoinvestInstituto']", 'null': 'True', 'blank': 'True'}),
            'nif': ('django.db.models.fields.CharField', [], {'max_length': '10L'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '60L'}),
            'sexenios': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sexo': ('django.db.models.fields.CharField', [], {'max_length': '6L'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '60L', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['viinvDB.AuthUser']", 'unique': 'True'})
        },
        u'viinvDB.grupoinvestsubareasinvestigacion': {
            'Meta': {'object_name': 'GrupoinvestSubareasinvestigacion', 'db_table': "u'GrupoInvest_subareasinvestigacion'"},
            'areaid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['viinvDB.GrupoinvestAreasinvestigacion']", 'db_column': "u'areaId_id'"}),
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '60L'})
        }
    }

    complete_apps = ['cvn']