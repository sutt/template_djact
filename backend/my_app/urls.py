from django.urls import path
from . import views

urlpatterns = [
    
    path('ok/', views.ok_view),
    path('list_tweets', views.list_tweets),

    path('mock_login', views.mock_login),
    path('mock_signup', views.mock_signup),

    path('test_permissions', views.test_permissions),
    path('auth_test_one', views.auth_test_one ),
    path('auth_test_two', views.auth_test_two ),
    path('auth_test_three', views.AuthTestThree.as_view() ),

    path('list_profile_tweets', views.list_profile_tweets),
    path('list_profile_tweets_serialized', views.ProtectedTweetList.as_view()),

    path('tweets/', views.TweetList.as_view()),
    path('tweets/<int:pk>', views.TweetDetail.as_view()),
]