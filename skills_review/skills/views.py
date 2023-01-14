from django.shortcuts import redirect, render

from . import models, recommend


def index_view(request):
    return render(request, "index.pug")


async def recommend_skills_from_job_title(request):
    job_title = request.POST["job-title"]
    skills = await recommend.get_job_skills(job_title)
    image_url = await recommend.get_job_image_url(job_title)
    context = {"skills": skills, "job_title": job_title, "image_url": image_url}
    return render(request, "recommend.pug", context=context)
