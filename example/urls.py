from django.urls import path
from django.conf.urls import include
from django.contrib import admin

from . import views
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.FlatpageView.as_view(), {'url': '/example/'}),
]
