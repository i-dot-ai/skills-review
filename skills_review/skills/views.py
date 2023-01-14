from asgiref.sync import sync_to_async
from django.shortcuts import redirect, render
from django.utils.text import slugify

from . import models, recommend


def index_view(request):
    return render(request, "index.pug")


def recommendation_exists(slug):
    return models.Recommendation.objects.filter(slug=slug).exists()


def save_recommendation(job_title, skills, image_url):
    recommendation = models.Recommendation(
        job_title=job_title,
        skills=skills,
        image_url=image_url,
    )
    recommendation.save()
    return recommendation


async def recommend_skills_from_job_title(request):
    job_title = request.POST["job-title"]
    slug = slugify(job_title)
    if not await sync_to_async(recommendation_exists)(slug):
        skills = await recommend.get_job_skills(job_title)
        image_url = await recommend.get_job_image_url(job_title)
        await sync_to_async(save_recommendation)(job_title, skills, image_url)
    return redirect(recommendation_view, slug=slug)


def recommendation_view(request, slug):
    recommendation = models.Recommendation.objects.get(slug=slug)
    context = {
        "skills": recommendation.skills,
        "job_title": recommendation.job_title,
        "image_url": recommendation.image_url,
    }
    return render(request, "recommend.pug", context=context)
