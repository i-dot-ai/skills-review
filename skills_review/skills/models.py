from django.db import models
from django_use_email_as_username.models import BaseUser, BaseUserManager


class User(BaseUser):
    objects = BaseUserManager()
    username = None

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)


class Skill(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)


class SkillSentence(models.Model):
    skill = models.ForeignKey(Skill, related_name="sentences", on_delete=models.CASCADE)


class Suggestion(models.Model):
    class Action(models.TextChoices):
        NOT_SKILL = ("Not a skill", "Not a skill")
        CHANGE_NAME = ("Change name", "Change name")
        NONE = ("None", "None")

    user = models.ForeignKey(User, related_name="suggestions", on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, related_name="suggestions", on_delete=models.CASCADE)
    action = models.CharField(max_length=256, choices=Action.choices, blank=True, null=True)
    comments = models.TextField()
