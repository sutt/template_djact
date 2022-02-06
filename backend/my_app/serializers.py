from dataclasses import fields
from rest_framework import serializers
from .models import Tweet

class TweetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tweet
        fields = ('uuid', 'user_string', 'content',)

# class ProtectedTweetSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Tweet
