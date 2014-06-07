# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Device'
        db.create_table(u'webapp_device', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_facebook.FacebookCustomUser'], null=True, blank=True)),
            ('mac', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('device', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('os', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('dump', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'webapp', ['Device'])

        # Adding unique constraint on 'Device', fields ['user', 'mac']
        db.create_unique(u'webapp_device', ['user_id', 'mac'])

        # Adding model 'DeviceToken'
        db.create_table(u'webapp_devicetoken', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('token', self.gf('django.db.models.fields.CharField')(unique=True, max_length=6)),
            ('mac', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
        ))
        db.send_create_signal(u'webapp', ['DeviceToken'])

        # Adding model 'CustomGroup'
        db.create_table(u'webapp_customgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'webapp', ['CustomGroup'])

        # Adding model 'UserGroup'
        db.create_table(u'webapp_usergroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_facebook.FacebookCustomUser'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.CustomGroup'])),
        ))
        db.send_create_signal(u'webapp', ['UserGroup'])

        # Adding unique constraint on 'UserGroup', fields ['user', 'group']
        db.create_unique(u'webapp_usergroup', ['user_id', 'group_id'])

        # Adding model 'Analytics'
        db.create_table(u'webapp_analytics', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_facebook.FacebookCustomUser'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'webapp', ['Analytics'])

        # Adding unique constraint on 'Analytics', fields ['user', 'key']
        db.create_unique(u'webapp_analytics', ['user_id', 'key'])

        # Adding model 'GroupAnalytics'
        db.create_table(u'webapp_groupanalytics', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.CustomGroup'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'webapp', ['GroupAnalytics'])

        # Adding unique constraint on 'GroupAnalytics', fields ['group', 'key']
        db.create_unique(u'webapp_groupanalytics', ['group_id', 'key'])

        # Adding model 'Usage'
        db.create_table(u'webapp_usage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.Device'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('load', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('uptime', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'webapp', ['Usage'])


    def backwards(self, orm):
        # Removing unique constraint on 'GroupAnalytics', fields ['group', 'key']
        db.delete_unique(u'webapp_groupanalytics', ['group_id', 'key'])

        # Removing unique constraint on 'Analytics', fields ['user', 'key']
        db.delete_unique(u'webapp_analytics', ['user_id', 'key'])

        # Removing unique constraint on 'UserGroup', fields ['user', 'group']
        db.delete_unique(u'webapp_usergroup', ['user_id', 'group_id'])

        # Removing unique constraint on 'Device', fields ['user', 'mac']
        db.delete_unique(u'webapp_device', ['user_id', 'mac'])

        # Deleting model 'Device'
        db.delete_table(u'webapp_device')

        # Deleting model 'DeviceToken'
        db.delete_table(u'webapp_devicetoken')

        # Deleting model 'CustomGroup'
        db.delete_table(u'webapp_customgroup')

        # Deleting model 'UserGroup'
        db.delete_table(u'webapp_usergroup')

        # Deleting model 'Analytics'
        db.delete_table(u'webapp_analytics')

        # Deleting model 'GroupAnalytics'
        db.delete_table(u'webapp_groupanalytics')

        # Deleting model 'Usage'
        db.delete_table(u'webapp_usage')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'django_facebook.facebookcustomuser': {
            'Meta': {'object_name': 'FacebookCustomUser'},
            'about_me': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'access_token': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'blog_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'facebook_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'facebook_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'facebook_open_graph': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_profile_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'new_token_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'raw_data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'website_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'webapp.analytics': {
            'Meta': {'unique_together': "(['user', 'key'],)", 'object_name': 'Analytics'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'webapp.customgroup': {
            'Meta': {'object_name': 'CustomGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'webapp.device': {
            'Meta': {'unique_together': "(['user', 'mac'],)", 'object_name': 'Device'},
            'device': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'dump': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mac': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']", 'null': 'True', 'blank': 'True'})
        },
        u'webapp.devicetoken': {
            'Meta': {'object_name': 'DeviceToken'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mac': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '6'})
        },
        u'webapp.groupanalytics': {
            'Meta': {'unique_together': "(['group', 'key'],)", 'object_name': 'GroupAnalytics'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.CustomGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'webapp.usage': {
            'Meta': {'object_name': 'Usage'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'load': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uptime': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'webapp.usergroup': {
            'Meta': {'unique_together': "(['user', 'group'],)", 'object_name': 'UserGroup'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webapp.CustomGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        }
    }

    complete_apps = ['webapp']