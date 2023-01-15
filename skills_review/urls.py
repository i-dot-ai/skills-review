from django.contrib import admin
from django.urls import include, path

from skills_review.skills import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("recommendation/<str:slug>/", views.recommendation_view, name="recommendation"),
    path("recommendation/<str:slug>/review/", views.review_view, name="review"),
    path("recommendation/<str:slug>/success/", views.success_view, name="thanks"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
]
