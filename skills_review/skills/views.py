import random

from django.shortcuts import redirect, render

from . import models


def index_view(request):
    return render(request, "index.html")


def make_mapping(skills):
    mapping = {}
    for skill in skills:
        mapping.setdefault(skill.level_1_name.strip(), {})
        mapping[skill.level_1_name].setdefault(skill.level_2_name.strip(), [])
        mapping[skill.level_1_name][skill.level_2_name].append(skill)
    return mapping


def skills_view(request):
    skills = models.Skill.objects.all()
    skills = random.sample(list(skills), k=len(skills))
    skills_map = make_mapping(skills)
    return render(request, "skills.html", {"skills_map": skills_map})


def skill_view(request, skill_slug):
    skill = models.Skill.objects.get(slug=skill_slug)
    if request.method == "GET":
        sentences = list(skill.sentences.all())
        actions = models.Suggestion.Action.values
        suggestions = models.Suggestion.objects.filter(skill=skill).all()
        return render(
            request,
            "skill.html",
            {"skill": skill, "sentences": sentences, "actions": actions, 'suggestions': suggestions},
        )
    else:
        data = request.POST
        user = request.user.is_authenticated and request.user or None
        suggestion = models.Suggestion(user=user, skill=skill, action=data["action"], comments=data["comments"])
        suggestion.save()
        return redirect("skill", skill_slug=skill_slug)
