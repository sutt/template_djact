from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework import generics
from .utils import utils

# adding for auth
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

# experimenting with these
from django.contrib.auth import authenticate as base_authenticate
from rest_framework_simplejwt.authentication import default_user_authentication_rule 
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.authentication import authenticate as drf_authenticate

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

@api_view(['GET'])
@permission_classes([permissions.DjangoModelPermissions])
def test_permissions(request):
    '''
        example protected function view
    '''
    return JsonResponse({'ok':True})

# from django.http import HttpRequest
# HttpRequest.body

@api_view(['GET', 'POST'])
# @permission_classes([permissions.DjangoModelPermissions])
def auth_test_one(request):
    
    utils.print_properties(request_obj=request)
    
    token_data = None
    if request.auth is not None:
        token_data = utils.token_analytics(request.auth)

    request_user = request.user.username

    try:
        import json
        request_user_2 = json.dumps(
                            request
                            .successful_authenticator
                            .get_user(request.auth)
                            )
    except:
        request_user_2 = None

    request_method = request.method

    request_body = {}
    if request.method == 'POST':
        request_body = str(request.body)

    return JsonResponse(
        {
            'token_data': token_data,
            'request_user': request_user,
            'request_user_2': request_user_2,
            'request_method': request_method,
            'request_body': request_body,
        }
        ,safe=False
    )

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def auth_test_two(request):
    return JsonResponse({
        'success': True,
        'endpoint': 'auth_test_two',
        # TODO - how to get permission classes here
        # 'route_permission_classes': str(self.permission_classes), 
        # 'route_authentication_classes': str(self.authentication_classes)
        }
    )

class AuthTestThree(generics.GenericAPIView):
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.AllowAny]
    
    # authentication_classes = []

    def get_queryset(self):
        pass  # required to override this property on this dummy view class

    def get(self, request, *args, **kwargs):
        return JsonResponse({
            'success': True,
            'endpoint': 'auth_test_two',
            'method': 'GET',
            'route_permission_classes': str(self.permission_classes), 
            'route_authentication_classes': str(self.authentication_classes)
        }
    )

    def post(self, request, *args, **kwargs):
        return JsonResponse({
            'success': True,
            'endpoint': 'auth_test_two',
            'method': 'GET',
            'route_permission_classes': str(self.permission_classes), 
            'route_authentication_classes': str(self.authentication_classes),
        }
    )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_profile_tweets(request):
    # [~] get request payload
    # [x] get user
    # [x] protect route
    # [x] ORM for query
    # print("\n".join(dir(request.user)))

    user_name = request.user.username
    
    profile_tweets = list(
        Tweet.objects
            .all()
            .filter(user_string=user_name)
            .values()
    )
    return JsonResponse(profile_tweets, safe=False)


class ProtectedTweetList(generics.ListAPIView):
    
    serializer_class = TweetSerializer
    queryset = Tweet.objects.all()
    
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    
    # authentication_classes = []
    
    def get(self, request, *args, **kwargs):
        utils.print_properties(
            request_obj=request,
            view_class=self,
        )
        return super().get(request, *args, **kwargs)


    
class TweetList(generics.ListCreateAPIView):
    
    serializer_class = TweetSerializer
    queryset = Tweet.objects.all()
    
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def post(self, request, *args, **kwargs):
        if request.user.username is not None:
            request.data['user_string'] = request.user.username
        return self.create(request, *args, **kwargs)


class TweetDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TweetSerializer
    queryset = Tweet.objects.all()




