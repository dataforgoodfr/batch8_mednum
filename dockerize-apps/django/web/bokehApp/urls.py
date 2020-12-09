from django.urls import path
from .import views

urlpatterns = [

path('bokeh/', views.home, name="home"),
]