"""Admin classes for the multilingual_survey app."""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from hvad.admin import TranslatableAdmin

from . import models


class SurveyAdmin(TranslatableAdmin):
    """Custom admin for the ``Survey`` model."""
    list_display = ['get_title', 'slug']

    def get_title(self, obj):
        return obj.title
    get_title.short_description = _('Title')


class SurveyQuestionAdmin(TranslatableAdmin):
    """Custom admin for the ``SurveyQuestion`` model."""
    list_display = ['get_title', 'slug', 'survey', 'is_multi_select',
                    'has_other_field', 'required', 'position']

    def get_title(self, obj):
        return obj.title
    get_title.short_description = _('Title')


class SurveyAnswerAdmin(TranslatableAdmin):
    """Custom admin for the ``SurveyAnswer`` model."""
    list_display = ['get_title', 'slug', 'question', 'position']

    def get_title(self, obj):
        return obj.title
    get_title.short_description = _('Title')


class SurveyResponseAdmin(admin.ModelAdmin):
    """Custom admin for the ``SurveyResponse`` model."""
    list_display = ['user_email', 'question', 'get_answer', 'date_created']

    def get_answer(self, obj):
        if obj.other_answer:
            return obj.other_answer
        answer_count = obj.answer.count()
        answer_string = ''
        for answer in obj.answer.all():
            if answer_string == '':
                answer_string += answer.title
            else:
                answer_string += ', {0}'.format(answer.title)
        answer_string = answer_string[:30] + unicode(answer_count)
        return answer_string
    get_answer.short_description = _('Answer')

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = _('User')


admin.site.register(models.SurveyResponse, SurveyResponseAdmin)
admin.site.register(models.SurveyAnswer, SurveyAnswerAdmin)
admin.site.register(models.SurveyQuestion, SurveyQuestionAdmin)
admin.site.register(models.Survey, SurveyAdmin)
