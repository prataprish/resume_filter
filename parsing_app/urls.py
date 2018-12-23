from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('index', views.index, name="index"),
    path('fetch', views.fetch),
    path('final', views.final),
    path('resume', views.resume)
]
