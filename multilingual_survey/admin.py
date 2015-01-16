"""Admin classes for the multilingual_survey app."""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from generic_positions.admin import GenericPositionsAdmin
from hvad.admin import TranslatableAdmin

from . import models


class SurveyAdmin(TranslatableAdmin):
    """Custom admin for the ``Survey`` model."""
    list_display = ['get_title', 'slug']

    def get_title(self, obj):
        return obj.__unicode__()
    get_title.short_description = _('Title')


class SurveyQuestionAdmin(GenericPositionsAdmin, TranslatableAdmin):
    """Custom admin for the ``SurveyQuestion`` model."""
    list_display = ['get_title', 'slug', 'survey', 'is_multi_select',
                    'has_other_field', 'required']
    list_filter = ['survey', ]

    def get_title(self, obj):
        return obj.__unicode__()
    get_title.short_description = _('Title')


class SurveyAnswerAdmin(GenericPositionsAdmin, TranslatableAdmin):
    """Custom admin for the ``SurveyAnswer`` model."""
    list_display = ['get_title', 'slug', 'question']
    list_filter = ['question', ]

    def get_title(self, obj):
        return obj.__unicode__()
    get_title.short_description = _('Title')


class SurveyResponseAdmin(admin.ModelAdmin):
    """Custom admin for the ``SurveyResponse`` model."""
    list_display = ['user_email', 'question', 'get_answer', 'date_created']

    def get_answer(self, obj):
        answer_string = ''
        for answer in obj.answer.all():
            if answer_string == '':
                answer_string += answer.__unicode__()
            else:
                answer_string += u', {0}'.format(answer.__unicode__())
        if obj.other_answer:
            if answer_string == '':
                answer_string += obj.other_answer
            else:
                answer_string += u', *{0}'.format(obj.other_answer)
        return answer_string[:30]
    get_answer.short_description = _('Answer')

    def user_email(self, obj):
        return obj.user.email if obj.user else 'Anonymous'
    user_email.short_description = _('User')


admin.site.register(models.SurveyResponse, SurveyResponseAdmin)
admin.site.register(models.SurveyAnswer, SurveyAnswerAdmin)
admin.site.register(models.SurveyQuestion, SurveyQuestionAdmin)
admin.site.register(models.Survey, SurveyAdmin)
