from django.utils.text import slugify
from django.shortcuts import redirect, render

from . import models, recommend


def index_view(request):
    return render(request, "index.pug")


async def recommend_skills_from_job_title(request):
    job_title = request.POST["job-title"]
    slug = slugify(job_title)
    if not models.Recommendation.objects.filter(slug=slug).exists():
        skills = await recommend.get_job_skills(job_title)
        image_url = await recommend.get_job_image_url(job_title)
        recommendation = models.Recommendation(
            job_title=job_title,
            skills=skills,
            image_url=image_url,
        )
        recommendation.save()
    return redirect(recommendation_view)


def recommendation_view(request, slug):
    recommendation = models.Recommendation.get(slug=slug)
    context = {"skills": recommendation.skills, "job_title": recommendation.job_title, "image_url": recommendation.image_url}
    return render(request, "recommend.pug", context=context)
