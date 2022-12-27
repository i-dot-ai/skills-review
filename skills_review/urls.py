from django.contrib import admin
from django.urls import include, path

from skills_review.skills import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("initialize/", views.initialize),
    path("skills", views.skills_view, name="skills"),
    path("skill/<str:skill_slug>", views.skill_view, name="skill"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
]
