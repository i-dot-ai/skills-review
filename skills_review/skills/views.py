import random

from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from . import models


def index_view(request):
    return render(request, "index.html")


def make_mapping(skills):
    mapping = {}
    for skill in skills:
        mapping.setdefault(skill.level_1_name.strip(), {})
        mapping[skill.level_1_name].setdefault(skill.level_2_name.strip(), [])
        mapping[skill.level_1_name][skill.level_2_name].append(skill.name.strip())
    return mapping


def skills_view(request):
    skills = models.Skill.objects.all()
    skills = random.sample(list(skills), k=len(skills))
    skills_map = make_mapping(skills)
    return render(request, "skills.html", {'skills_map': skills_map})