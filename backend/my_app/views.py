from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Tweet

# Create your views here.

def ok_view(request):
    return HttpResponse("ok!")

def list_tweets(request):
    tweets = Tweet.objects.all().values()
    tweets_list = list(tweets)
    return JsonResponse(tweets_list, safe=False)


