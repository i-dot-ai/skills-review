import random

from django.shortcuts import render, redirect
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


def skill_view(request, skill_slug):
    skill = models.Skill.objects.get(slug=skill_slug)
    if request.method == "GET":
        sentences = list(skill.sentences.all())
        actions = models.Suggestion.Action.values
        return render(request, "skill.html", {'skill': skill, 'sentences': sentences, 'actions': actions})
    else:
        data = request.POST
        user = request.user.is_authenticated and request.user or None
        suggestion = models.Suggestion(user=user, skill=skill, action=data['action'], comments=data['comments'])
        suggestion.save()
        return redirect("skill", skill_slug= skill_slug)
