from django.db import models
from django.utils.text import slugify
from django_use_email_as_username.models import BaseUser, BaseUserManager


class User(BaseUser):
    objects = BaseUserManager()
    username = None

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)


class Recommendation(models.Model):
    job_title = models.CharField(max_length=256, unique=True)
    slug = models.CharField(max_length=256, unique=True, primary_key=True)
    skills = models.JSONField(default=list)
    image_url = models.CharField(max_length=256, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name.replace("|", "_"))
        return super().save(*args, **kwargs)
