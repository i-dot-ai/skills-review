from django.contrib import admin

from . import models

admin.site.register(models.Skill)
admin.site.register(models.SkillSentence)
admin.site.register(models.Suggestion)

admin.site.register(models.User)
