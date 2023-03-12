from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.mark,name="mark"),
    path('register', views.register,name="register"),
    #access the laptop camera
    path('video_feed', views.video_feed, name='video_feed'),

]