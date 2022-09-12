from django.db import models
from django.utils.text import slugify
from django_use_email_as_username.models import BaseUser, BaseUserManager


class User(BaseUser):
    objects = BaseUserManager()
    username = None

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)


class Skill(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.CharField(max_length=256, unique=True, primary_key=True)
    level_1_name = models.CharField(max_length=256)
    level_2_name = models.CharField(max_length=256)
    has_delete_flag = models.BooleanField(blank=True, null=True)
    has_rename_flag = models.BooleanField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name.replace("|", "_"))
        return super().save(*args, **kwargs)


class SkillSentence(models.Model):
    skill = models.ForeignKey(Skill, related_name="sentences", on_delete=models.CASCADE)
    text = models.CharField(max_length=256)


class Suggestion(models.Model):
    class Flag(models.TextChoices):
        NOT_SKILL = ("Not a skill", "Not a skill")
        WRONG_NAME = ("Wrong name", "Wrong name")
        MULTIPLE_SKILLS = ("Multiple skills", "Multiple skills")
        WRONG_CATEGORY = ("Wrong category", "Wrong category")
        NONE = ("None", "None")

    user = models.ForeignKey(
        User,
        related_name="suggestions",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    skill = models.ForeignKey(Skill, related_name="suggestions", on_delete=models.CASCADE)
    flag = models.CharField(max_length=256, choices=Flag.choices, blank=True, null=True)
    comments = models.TextField()

    _error_flags = set([Flag.NOT_SKILL])
    _warning_flags = set([Flag.WRONG_NAME, Flag.MULTIPLE_SKILLS, Flag.WRONG_CATEGORY])

    def save(self, *args, **kwargs):
        if self.flag in self._error_flags:
            self.skill.has_delete_flag = True
        elif self.flag in self._warning_flags:
            self.skill.has_rename_flag = True
        self.skill.save()
        return super().save(*args, **kwargs)
