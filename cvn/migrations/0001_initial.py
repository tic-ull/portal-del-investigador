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
            ('fecha', self.gf('django.db.models.fields.DateField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user_profile', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.UserProfile'], unique=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('is_inserted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'cvn', ['CVN'])

        # Adding model 'Articulo'
        db.create_table(u'cvn_articulo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('fecha', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('nombre_publicacion', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('volumen', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('numero', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('pagina_inicial', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('pagina_final', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('autores', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('issn', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('deposito_legal', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'cvn', ['Articulo'])

        # Adding M2M table for field user_profile on 'Articulo'
        m2m_table_name = db.shorten_name(u'cvn_articulo_user_profile')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('articulo', models.ForeignKey(orm[u'cvn.articulo'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'core.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['articulo_id', 'userprofile_id'])

        # Adding model 'Libro'
        db.create_table(u'cvn_libro', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('fecha', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('nombre_publicacion', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('volumen', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('numero', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('pagina_inicial', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('pagina_final', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('autores', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('issn', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('deposito_legal', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'cvn', ['Libro'])

        # Adding M2M table for field user_profile on 'Libro'
        m2m_table_name = db.shorten_name(u'cvn_libro_user_profile')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('libro', models.ForeignKey(orm[u'cvn.libro'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'core.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['libro_id', 'userprofile_id'])

        # Adding model 'Capitulo'
        db.create_table(u'cvn_capitulo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('fecha', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('nombre_publicacion', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('volumen', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('numero', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('pagina_inicial', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('pagina_final', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('autores', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('issn', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('deposito_legal', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'cvn', ['Capitulo'])

        # Adding M2M table for field user_profile on 'Capitulo'
        m2m_table_name = db.shorten_name(u'cvn_capitulo_user_profile')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('capitulo', models.ForeignKey(orm[u'cvn.capitulo'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'core.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['capitulo_id', 'userprofile_id'])

        # Adding model 'Congreso'
        db.create_table(u'cvn_congreso', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('fecha_de_inicio', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('fecha_de_fin', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('nombre_del_congreso', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('ciudad_de_realizacion', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('autores', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('fecha', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('ambito', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('otro_ambito', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('deposito_legal', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('publicacion_acta_congreso', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'cvn', ['Congreso'])

        # Adding M2M table for field user_profile on 'Congreso'
        m2m_table_name = db.shorten_name(u'cvn_congreso_user_profile')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('congreso', models.ForeignKey(orm[u'cvn.congreso'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'core.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['congreso_id', 'userprofile_id'])

        # Adding model 'Proyecto'
        db.create_table(u'cvn_proyecto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('numero_de_investigadores', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('autores', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('fecha_de_inicio', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('fecha_de_fin', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('duracion', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('ambito', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('otro_ambito', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('cod_segun_financiadora', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('cuantia_total', self.gf('django.db.models.fields.CharField')(max_length=19, null=True, blank=True)),
            ('cuantia_subproyecto', self.gf('django.db.models.fields.CharField')(max_length=19, null=True, blank=True)),
            ('porcentaje_en_subvencion', self.gf('django.db.models.fields.CharField')(max_length=19, null=True, blank=True)),
            ('porcentaje_en_credito', self.gf('django.db.models.fields.CharField')(max_length=19, null=True, blank=True)),
            ('porcentaje_mixto', self.gf('django.db.models.fields.CharField')(max_length=19, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'cvn', ['Proyecto'])

        # Adding M2M table for field user_profile on 'Proyecto'
        m2m_table_name = db.shorten_name(u'cvn_proyecto_user_profile')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('proyecto', models.ForeignKey(orm[u'cvn.proyecto'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'core.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['proyecto_id', 'userprofile_id'])

        # Adding model 'Convenio'
        db.create_table(u'cvn_convenio', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('autores', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('fecha_de_inicio', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('fecha_de_fin', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('duracion', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('ambito', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('otro_ambito', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('cod_segun_financiadora', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('cuantia_total', self.gf('django.db.models.fields.CharField')(max_length=19, null=True, blank=True)),
            ('cuantia_subproyecto', self.gf('django.db.models.fields.CharField')(max_length=19, null=True, blank=True)),
            ('porcentaje_en_subvencion', self.gf('django.db.models.fields.CharField')(max_length=19, null=True, blank=True)),
            ('porcentaje_en_credito', self.gf('django.db.models.fields.CharField')(max_length=19, null=True, blank=True)),
            ('porcentaje_mixto', self.gf('django.db.models.fields.CharField')(max_length=19, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'cvn', ['Convenio'])

        # Adding M2M table for field user_profile on 'Convenio'
        m2m_table_name = db.shorten_name(u'cvn_convenio_user_profile')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('convenio', models.ForeignKey(orm[u'cvn.convenio'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'core.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['convenio_id', 'userprofile_id'])

        # Adding model 'TesisDoctoral'
        db.create_table(u'cvn_tesisdoctoral', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('fecha', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('autor', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('universidad_que_titula', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('codirector', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'cvn', ['TesisDoctoral'])

        # Adding M2M table for field user_profile on 'TesisDoctoral'
        m2m_table_name = db.shorten_name(u'cvn_tesisdoctoral_user_profile')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tesisdoctoral', models.ForeignKey(orm[u'cvn.tesisdoctoral'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'core.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tesisdoctoral_id', 'userprofile_id'])


    def backwards(self, orm):
        # Deleting model 'CVN'
        db.delete_table(u'cvn_cvn')

        # Deleting model 'Articulo'
        db.delete_table(u'cvn_articulo')

        # Removing M2M table for field user_profile on 'Articulo'
        db.delete_table(db.shorten_name(u'cvn_articulo_user_profile'))

        # Deleting model 'Libro'
        db.delete_table(u'cvn_libro')

        # Removing M2M table for field user_profile on 'Libro'
        db.delete_table(db.shorten_name(u'cvn_libro_user_profile'))

        # Deleting model 'Capitulo'
        db.delete_table(u'cvn_capitulo')

        # Removing M2M table for field user_profile on 'Capitulo'
        db.delete_table(db.shorten_name(u'cvn_capitulo_user_profile'))

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
        u'core.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'documento': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rrhh_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'cvn.articulo': {
            'Meta': {'object_name': 'Articulo'},
            'autores': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deposito_legal': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'issn': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'nombre_publicacion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'numero': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pagina_final': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pagina_inicial': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_profile': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.UserProfile']", 'null': 'True', 'blank': 'True'}),
            'volumen': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'cvn.capitulo': {
            'Meta': {'object_name': 'Capitulo'},
            'autores': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deposito_legal': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'issn': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'nombre_publicacion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'numero': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pagina_final': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pagina_inicial': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_profile': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.UserProfile']", 'null': 'True', 'blank': 'True'}),
            'volumen': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'cvn.congreso': {
            'Meta': {'ordering': "['-fecha_de_inicio', 'titulo']", 'object_name': 'Congreso'},
            'ambito': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'autores': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ciudad_de_realizacion': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deposito_legal': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_de_fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_de_inicio': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre_del_congreso': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'otro_ambito': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'publicacion_acta_congreso': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_profile': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.UserProfile']", 'null': 'True', 'blank': 'True'})
        },
        u'cvn.convenio': {
            'Meta': {'ordering': "['-fecha_de_inicio', 'titulo']", 'object_name': 'Convenio'},
            'ambito': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'autores': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cod_segun_financiadora': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cuantia_subproyecto': ('django.db.models.fields.CharField', [], {'max_length': '19', 'null': 'True', 'blank': 'True'}),
            'cuantia_total': ('django.db.models.fields.CharField', [], {'max_length': '19', 'null': 'True', 'blank': 'True'}),
            'duracion': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_de_fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_de_inicio': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'otro_ambito': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'porcentaje_en_credito': ('django.db.models.fields.CharField', [], {'max_length': '19', 'null': 'True', 'blank': 'True'}),
            'porcentaje_en_subvencion': ('django.db.models.fields.CharField', [], {'max_length': '19', 'null': 'True', 'blank': 'True'}),
            'porcentaje_mixto': ('django.db.models.fields.CharField', [], {'max_length': '19', 'null': 'True', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_profile': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.UserProfile']", 'null': 'True', 'blank': 'True'})
        },
        u'cvn.cvn': {
            'Meta': {'object_name': 'CVN'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cvn_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_inserted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_profile': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.UserProfile']", 'unique': 'True'}),
            'xml_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'cvn.libro': {
            'Meta': {'object_name': 'Libro'},
            'autores': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deposito_legal': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'issn': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'nombre_publicacion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'numero': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pagina_final': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pagina_inicial': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_profile': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.UserProfile']", 'null': 'True', 'blank': 'True'}),
            'volumen': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'cvn.proyecto': {
            'Meta': {'ordering': "['-fecha_de_inicio', 'titulo']", 'object_name': 'Proyecto'},
            'ambito': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'autores': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cod_segun_financiadora': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cuantia_subproyecto': ('django.db.models.fields.CharField', [], {'max_length': '19', 'null': 'True', 'blank': 'True'}),
            'cuantia_total': ('django.db.models.fields.CharField', [], {'max_length': '19', 'null': 'True', 'blank': 'True'}),
            'duracion': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_de_fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_de_inicio': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero_de_investigadores': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'otro_ambito': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'porcentaje_en_credito': ('django.db.models.fields.CharField', [], {'max_length': '19', 'null': 'True', 'blank': 'True'}),
            'porcentaje_en_subvencion': ('django.db.models.fields.CharField', [], {'max_length': '19', 'null': 'True', 'blank': 'True'}),
            'porcentaje_mixto': ('django.db.models.fields.CharField', [], {'max_length': '19', 'null': 'True', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_profile': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.UserProfile']", 'null': 'True', 'blank': 'True'})
        },
        u'cvn.tesisdoctoral': {
            'Meta': {'ordering': "['-fecha', 'titulo']", 'object_name': 'TesisDoctoral'},
            'autor': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'codirector': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'titulo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'universidad_que_titula': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_profile': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.UserProfile']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cvn']