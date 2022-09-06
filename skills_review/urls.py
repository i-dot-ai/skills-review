from django.contrib import admin
from django.urls import include, path

from skills_review.skills import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("skills", views.skills_view, name="skills"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
]
