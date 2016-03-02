# flake8: noqa
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SurveyTranslation'
        db.create_table(u'multilingual_survey_survey_translation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['multilingual_survey.Survey'])),
        ))
        db.send_create_signal(u'multilingual_survey', ['SurveyTranslation'])

        # Adding unique constraint on 'SurveyTranslation', fields ['language_code', 'master']
        db.create_unique(u'multilingual_survey_survey_translation', ['language_code', 'master_id'])

        # Adding model 'Survey'
        db.create_table(u'multilingual_survey_survey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=256)),
        ))
        db.send_create_signal(u'multilingual_survey', ['Survey'])

        # Adding model 'SurveyQuestionTranslation'
        db.create_table(u'multilingual_survey_surveyquestion_translation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['multilingual_survey.SurveyQuestion'])),
        ))
        db.send_create_signal(u'multilingual_survey', ['SurveyQuestionTranslation'])

        # Adding unique constraint on 'SurveyQuestionTranslation', fields ['language_code', 'master']
        db.create_unique(u'multilingual_survey_surveyquestion_translation', ['language_code', 'master_id'])

        # Adding model 'SurveyQuestion'
        db.create_table(u'multilingual_survey_surveyquestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=256)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questions', to=orm['multilingual_survey.Survey'])),
            ('is_multi_select', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_other_field', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'multilingual_survey', ['SurveyQuestion'])

        # Adding unique constraint on 'SurveyQuestion', fields ['slug', 'survey']
        db.create_unique(u'multilingual_survey_surveyquestion', ['slug', 'survey_id'])

        # Adding model 'SurveyAnswerTranslation'
        db.create_table(u'multilingual_survey_surveyanswer_translation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['multilingual_survey.SurveyAnswer'])),
        ))
        db.send_create_signal(u'multilingual_survey', ['SurveyAnswerTranslation'])

        # Adding unique constraint on 'SurveyAnswerTranslation', fields ['language_code', 'master']
        db.create_unique(u'multilingual_survey_surveyanswer_translation', ['language_code', 'master_id'])

        # Adding model 'SurveyAnswer'
        db.create_table(u'multilingual_survey_surveyanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=256)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['multilingual_survey.SurveyQuestion'])),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'multilingual_survey', ['SurveyAnswer'])

        # Adding unique constraint on 'SurveyAnswer', fields ['slug', 'question']
        db.create_unique(u'multilingual_survey_surveyanswer', ['slug', 'question_id'])

        # Adding model 'SurveyResponse'
        db.create_table(u'multilingual_survey_surveyresponse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='responses', null=True, to=orm['auth.User'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='responses', null=True, to=orm['multilingual_survey.SurveyQuestion'])),
            ('other_answer', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'multilingual_survey', ['SurveyResponse'])

        # Adding M2M table for field answer on 'SurveyResponse'
        m2m_table_name = db.shorten_name(u'multilingual_survey_surveyresponse_answer')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('surveyresponse', models.ForeignKey(orm[u'multilingual_survey.surveyresponse'], null=False)),
            ('surveyanswer', models.ForeignKey(orm[u'multilingual_survey.surveyanswer'], null=False))
        ))
        db.create_unique(m2m_table_name, ['surveyresponse_id', 'surveyanswer_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'SurveyAnswer', fields ['slug', 'question']
        db.delete_unique(u'multilingual_survey_surveyanswer', ['slug', 'question_id'])

        # Removing unique constraint on 'SurveyAnswerTranslation', fields ['language_code', 'master']
        db.delete_unique(u'multilingual_survey_surveyanswer_translation', ['language_code', 'master_id'])

        # Removing unique constraint on 'SurveyQuestion', fields ['slug', 'survey']
        db.delete_unique(u'multilingual_survey_surveyquestion', ['slug', 'survey_id'])

        # Removing unique constraint on 'SurveyQuestionTranslation', fields ['language_code', 'master']
        db.delete_unique(u'multilingual_survey_surveyquestion_translation', ['language_code', 'master_id'])

        # Removing unique constraint on 'SurveyTranslation', fields ['language_code', 'master']
        db.delete_unique(u'multilingual_survey_survey_translation', ['language_code', 'master_id'])

        # Deleting model 'SurveyTranslation'
        db.delete_table(u'multilingual_survey_survey_translation')

        # Deleting model 'Survey'
        db.delete_table(u'multilingual_survey_survey')

        # Deleting model 'SurveyQuestionTranslation'
        db.delete_table(u'multilingual_survey_surveyquestion_translation')

        # Deleting model 'SurveyQuestion'
        db.delete_table(u'multilingual_survey_surveyquestion')

        # Deleting model 'SurveyAnswerTranslation'
        db.delete_table(u'multilingual_survey_surveyanswer_translation')

        # Deleting model 'SurveyAnswer'
        db.delete_table(u'multilingual_survey_surveyanswer')

        # Deleting model 'SurveyResponse'
        db.delete_table(u'multilingual_survey_surveyresponse')

        # Removing M2M table for field answer on 'SurveyResponse'
        db.delete_table(db.shorten_name(u'multilingual_survey_surveyresponse_answer'))


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'multilingual_survey.survey': {
            'Meta': {'object_name': 'Survey'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '256'})
        },
        u'multilingual_survey.surveyanswer': {
            'Meta': {'ordering': "('position',)", 'unique_together': "(('slug', 'question'),)", 'object_name': 'SurveyAnswer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': u"orm['multilingual_survey.SurveyQuestion']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '256'})
        },
        u'multilingual_survey.surveyanswertranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'SurveyAnswerTranslation', 'db_table': "u'multilingual_survey_surveyanswer_translation'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['multilingual_survey.SurveyAnswer']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'multilingual_survey.surveyquestion': {
            'Meta': {'ordering': "('position',)", 'unique_together': "(('slug', 'survey'),)", 'object_name': 'SurveyQuestion'},
            'has_other_field': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_multi_select': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '256'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': u"orm['multilingual_survey.Survey']"})
        },
        u'multilingual_survey.surveyquestiontranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'SurveyQuestionTranslation', 'db_table': "u'multilingual_survey_surveyquestion_translation'"},
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['multilingual_survey.SurveyQuestion']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'multilingual_survey.surveyresponse': {
            'Meta': {'ordering': "('question__position',)", 'object_name': 'SurveyResponse'},
            'answer': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['multilingual_survey.SurveyAnswer']", 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'other_answer': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'responses'", 'null': 'True', 'to': u"orm['multilingual_survey.SurveyQuestion']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'responses'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'multilingual_survey.surveytranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'SurveyTranslation', 'db_table': "u'multilingual_survey_survey_translation'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['multilingual_survey.Survey']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['multilingual_survey']
