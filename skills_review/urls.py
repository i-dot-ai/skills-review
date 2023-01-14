from django.contrib import admin
from django.urls import include, path

from skills_review.skills import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("recommendation/", views.recommend_skills_from_job_title),
    path("recommendation/<str:slug>/", views.recommendation_view),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
]
