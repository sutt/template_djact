from django.urls import path
from . import views

urlpatterns = [
    path('api/auth/signup/', views.CreateUserView.as_view()),
    
]