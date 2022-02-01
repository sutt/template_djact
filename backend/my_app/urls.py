from django.urls import path
from . import views

urlpatterns = [
    path('ok/', views.ok_view),
    path('tweets', views.list_tweets),
]