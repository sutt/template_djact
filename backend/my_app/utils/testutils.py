from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from ..models import Tweet
import requests
import json
import time

class CustomClient:

    def __init__(self, 
        live_server_url=None,
        explicit_localhost_ip=True,
        ):

        self.method =  'GET'
        self.headers = {'Content-Type': 'application/json'}
        self.data = None
        self.authToken = None

        if live_server_url is None:
            live_server_url = 'http://localhost:8000'
        
        if explicit_localhost_ip:
            # http://localhost:58888 -> http://127.0.0.1:58888/
            # because this is faster when dealing with DNS from 
            # cold-started requests library
            live_server_url = live_server_url.replace(
                                    'localhost', '127.0.0.1'
                                    )
        live_server_url += '/'
        self.base_url = live_server_url

    def get_login_token(self, 
            username='test_user',
            password='password'
        ):
        
        endpoint = 'api/token/'
        method = 'POST'
        data = {'username': 'test_user', 'password': 'password'}
        token_res = self.make_request(
            endpoint=endpoint, method=method, data=data
            )
        
        assert token_res is not None
        assert isinstance(token_res.get('access'), str)
        assert isinstance(token_res.get('refresh'), str)
        
        return token_res

    @staticmethod
    def make_auth_header(access_token):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'  # set to `JWT` in settings.py config
        }

    def make_request(
        self,
        endpoint,
        method=None,
        params=None,
        headers=None,
        data=None,
        expect_html=False,
        verbose=False,
        return_obj=False,
        ):
        
        if method is None: method = self.method
        if headers is None: headers = self.headers
        if data is None: data = self.data

        url = self.base_url + endpoint
        
        if params is not None:
            url += params

        r = requests.request(
            method,
            url=url, 
            data=json.dumps(data),
            headers=headers,
            )

        if verbose:
            print('\n--------')
            print(f'url: {url}')

        if return_obj: return r

        if not(r.ok):
            try: 
                if verbose: print(f'request failed {r.status_code}')
                if verbose: print(f'content: {r.content}')
            except: pass
            return

        if expect_html:
            try: response = r.content
            except: 
                if verbose: print(f'could not get content from expect_html response')
        
        else:
            try: response = r.json()
            except Exception as e:
                if verbose: print(f'failed to parse response json: {e}')
                if verbose: print(r.content)
                return
        
        return response

class DbUtil:

    def __init__(self):
        self.UserModel = get_user_model()
        

    def make_tweet(
        self,
        content,
        user_string=None,
    ):
        tweet = Tweet(content=content, user_string=user_string)
        tweet.save()

    def make_user(
        self,
        username,
        password='password',
        ):
        hashed_password = make_password(password)
        User = get_user_model()
        user = User(username=username, password=hashed_password)
        user.save()

    def make_user_with_tweets(
        
        ):
        # TODO - make random lorem ipsum tweets
        pass

    def check_for_user(
        self,
        username,
        ):

        try: 
            query = self.UserModel.objects.get(username=username)
            assert query.username == username
            return True
        except: 
            return False
        

    @classmethod
    def delete_tweets(
        cls,
        number=0,
        percentage=0,
        random=False,
        latest=False,
        earliest=False,
        **kwargs,
        ):

        if (number <= 0) and (percentage <= 0):
            raise Exception("must supply `number` or `percentage` value to delete")
        if (percentage > 1):
            raise Exception("`percentage` is a float (0,1]; currently too high")

        # TODO - select the values and delete them
        amount = 0
        total = 10 # TODO
        if number > 0: 
            amount = number
        else:
            amount = round(total*percentage, 0)

        keys = ['user_string', 'content', 'pk']
        conditions = {}
        for key in keys:
            if kwargs.get(key) is not None:
                conditions[key] = kwargs.get(key)
        