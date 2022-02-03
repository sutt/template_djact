from django.urls import path
from . import views

urlpatterns = [
    
    path('ok/', views.ok_view),
    path('list_tweets', views.list_tweets),

    path('mock_login', views.mock_login),

    path('tweets/', views.TweetList.as_view()),
    path('tweets/<int:pk>', views.TweetDetail.as_view()),
]