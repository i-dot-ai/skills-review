from asgiref.sync import sync_to_async
from django.shortcuts import redirect, render
from django.utils.text import slugify

from . import models, recommend, taxonomy


def recommendation_exists(slug, source):
    return models.Recommendation.objects.filter(slug=slug, source=source).exists()


def save_recommendation(job_title, skills, image_url, source):
    recommendation = models.Recommendation(
        job_title=job_title,
        skills=skills,
        image_url=image_url,
    )
    recommendation.save()
    return recommendation


async def index_view(request, source="openai"):
    if request.method == "GET":
        context = {"source": source}
        return render(request, "index.pug", context=context)
    elif request.method == "POST":
        job_title = request.POST["job-title"]
        source = request.POST["source"]
        slug = slugify(job_title)
        if not slug:
            context = dict(errors={"job-title": ["Please enter a job title"]}, source=source)
            return render(request, "index.pug", context=context)
        if not await sync_to_async(recommendation_exists)(slug, source):
            if source == "openai":
                skills = await recommend.get_job_skills(job_title)
                image_url = await recommend.get_job_image_url(job_title)
            else:
                skills = taxonomy.recommend_relevant_job_skills(job_title)
                image_url = None
            await sync_to_async(save_recommendation)(job_title, skills, image_url, source)
        return redirect("recommendation", slug=slug)


def recommendation_view(request, slug):
    recommendation = models.Recommendation.objects.get(slug=slug)
    context = {"recommendation": recommendation}
    return render(request, "recommend.pug", context=context)


def review_view(request, slug):
    recommendation = models.Recommendation.objects.get(slug=slug)
    if request.method == "GET":
        context = {"recommendation": recommendation}
        return render(request, "review.pug", context=context)
    elif request.method == "POST":
        incorrect_skills = set(request.POST.keys())
        if incorrect_skills.__contains__("csrfmiddlewaretoken"):
            incorrect_skills.remove("csrfmiddlewaretoken")
        skills = set(recommendation.skills)
        correct_skills = skills - incorrect_skills
        recommendation.good_skills = list(correct_skills)
        recommendation.bad_skills = list(incorrect_skills)
        recommendation.save()
        return redirect("success", slug=slug)


def success_view(request, slug):
    recommendation = models.Recommendation.objects.get(slug=slug)
    context = {"source": recommendation.source}
    return render(request, "success.pug", context=context)
