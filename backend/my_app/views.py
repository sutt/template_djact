from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework import generics

from .models import Tweet
from .serializers import TweetSerializer

# Create your views here.

def ok_view(request):
    return HttpResponse("ok!")

def list_tweets(request):
    tweets = Tweet.objects.all().values()
    tweets_list = list(tweets)
    return JsonResponse(tweets_list, safe=False)

def mock_login(request):
    return JsonResponse({'loggedIn':True, 'username': 'mock_user'})

def mock_signup(request):
    return JsonResponse({'loggedIn':True, 'username': 'mock_user'})

class TweetList(generics.ListCreateAPIView):
    serializer_class = TweetSerializer
    queryset = Tweet.objects.all()

class TweetDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TweetSerializer
    queryset = Tweet.objects.all()




