from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.FlatpageView.as_view(), {"url": "/example/"}),
]
