import requests
import json

### Defaults

base        = "http://127.0.0.1:8000/"  # much faster than localhost
endpoint    = "auth_test_one"

method = 'GET'

headers =   {'Content-Type': 'application/json'}
                
def make_auth_header(token):
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

authtoken = None

if authtoken is not None:
    headers = make_auth_header(authtoken)

data = {}

### Shared Function


def make_request(
    url=base + endpoint,
    method=method,
    headers=headers,
    data=data,
    expect_html=False,
    verbose=False,
    return_obj=False,
    ):
    '''
        make request and process it
    '''

    
    r = requests.request(method,
                        url, 
                        data=json.dumps(data),
                        headers=headers,
                        )

    if return_obj: return r

    if not(r.ok):
        try: 
            print(f'request failed {r.status_code}')
            if verbose: print(f'content: {r.content}')
        except: pass
        return

    if expect_html:
        try: response = r.content
        except: print(f'could not get content from expect_html response')
    
    else:
        try: response = r.json()
        except Exception as e:
            print(f'failed to parse response json: {e}')
            if verbose: print(r.content)
            return
    
    return response



### Build Tests here

def test_method_log():
    
    method = 'GET'
    res = make_request(method=method)
    if res is None: raise
    assert res.get('request_method', None) == method

    method = 'POST'
    res = make_request(method=method)
    if res is None: raise
    assert res.get('request_method', None) == method

def test_post_body():
    
    method = 'POST'
    data = {'key1': 'value1', 'd1': {'a':1, 'b':2}}
    res = make_request(method=method, data=data)
    if res is None: raise
    
    assert res.get('request_body', None) != {}

    assert isinstance(res.get('request_body', None), str)

def test_patch_fails():

    method = 'PATCH'
    res = make_request(method=method)
    assert res is None

def test_login_basic():

    endpoint = 'api/token/'
    method = 'POST'
    data = {'username': 'test_mock_1', 'password': 'password'}
    token_res = make_request(url=base + endpoint, method=method, data=data)
    assert token_res is not None
    assert isinstance(token_res.get('access', None), str)
    assert isinstance(token_res.get('refresh', None), str)

    endpoint = 'auth_test_two'
    protected_res = make_request(url=base + endpoint)
    assert protected_res is None
    
    endpoint = 'auth_test_two'
    headers = make_auth_header(token_res['access'])
    protected_res = make_request(url=base + endpoint, headers=headers,) # verbose=True)
    assert protected_res is not None
    assert protected_res.get('success', None) == True 

def test_bad_login_1():
    
    # login request with wrong login values in the body
    endpoint = 'api/token/'
    method = 'POST'
    data = {'username': 'wrong_user', 'password': 'wrong_password'}
    res_obj = make_request(url=base + endpoint, method=method, data=data, return_obj=True)
    
    assert res_obj.status_code == 401
    # msg = res_obj.json()
    # assert msg['detail'] == 'No active account found with the given credentials'
    
    # no body in the login request
    endpoint = 'api/token/'
    method = 'POST'
    res_obj = make_request(url=base + endpoint, method=method, return_obj=True)

    assert res_obj.status_code == 400
    
def test_jwt_response_1():
    
    # get jwt
    endpoint = 'api/token/'
    method = 'POST'
    data = {'username': 'test_mock_1', 'password': 'password'}
    token_res = make_request(url=base + endpoint, method=method, data=data)
    
    # GET works with no auth for IsAuthenticatedOrReadOnly
    # use response to verify the backend route has a certain permission
    endpoint = 'auth_test_three'
    res_obj = make_request(url=base + endpoint, return_obj=True)
    assert res_obj.status_code == 200
    res = res_obj.json()
    assert res.get('route_permission_classes', None) == "[<class 'rest_framework.permissions.IsAuthenticatedOrReadOnly'>]"

    # POST failes on these permissions
    endpoint = 'auth_test_three'
    method = 'POST'
    res_obj = make_request(url=base + endpoint, method=method, return_obj=True)
    assert res_obj.status_code == 401

    # POST goes thru with proper auth headers
    endpoint = 'auth_test_three'
    method = 'POST'
    headers = make_auth_header(token_res['access'])
    res_obj = make_request(url=base + endpoint, method=method, headers=headers, return_obj=True)
    assert res_obj.status_code == 200

    # malformed token 401
    endpoint = 'auth_test_three'
    method = 'POST'
    headers = make_auth_header(token_res['access'][:-1])
    res_obj = make_request(url=base + endpoint, method=method, headers=headers, return_obj=True)
    assert res_obj.status_code == 401
    # "detail":"Given token not valid for any token type"
    
    # expired token
    expired_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ0Mjk1MTU0LCJpYXQiOjE2NDQyOTQ4NTQsImp0aSI6ImJlZmNlMGMxN2VlOTRmYjk4YWE2OGY5ODBiM2E0YzUyIiwidXNlcl9pZCI6Mn0.VGlN_J8ftJ7JjW1yNlEwkiPnhX-ZE-rEn2szrhXrYvs"
    endpoint = 'auth_test_three'
    method = 'POST'
    headers = make_auth_header(expired_token)
    res_obj = make_request(url=base + endpoint, method=method, headers=headers, return_obj=True)
    assert res_obj.status_code == 401


def test_new_tweet_is_protected():

    # un-authed GET to this route should work
    endpoint = 'tweets/'
    res = make_request(url=base + endpoint)
    assert res is not None
    
    # un-authed POST to this route should 401
    endpoint = 'tweets/'
    method = 'POST'
    data = {'username': 'test_mock_1', 'content':'testing command'}
    res = make_request(url=base + endpoint, method=method, data=data)
    assert res is None

    # get jwt
    endpoint = 'api/token/'
    method = 'POST'
    data = {'username': 'test_mock_1', 'password': 'password'}
    token_res = make_request(url=base + endpoint, method=method, data=data)
    assert token_res is not None

    # authed POST should work returning an object
    endpoint = 'tweets/'
    method = 'POST'
    data = {'username':'test_mock_1', 'content':'testing command'}
    headers = make_auth_header(token_res['access'])
    res = make_request(url=base + endpoint, method=method, data=data, headers=headers)
    assert res is not None
    assert res.get('user_string', None) == 'test_mock_1'


def test_new_tweet_uses_auth_user():

    # get jwt
    endpoint = 'api/token/'
    method = 'POST'
    data = {'username': 'test_mock_1', 'password': 'password'}
    token_res = make_request(url=base + endpoint, method=method, data=data)
    assert token_res is not None

    # make a new tweet with:
    # auth user: test_mock_1
    # request payload: username: wrong_user
    endpoint = 'tweets/'
    method = 'POST'
    data = {'username': 'wrong_user', 'content':'testing command (wrong user)'}
    headers = make_auth_header(token_res['access'])
    res = make_request(url=base + endpoint, method=method, data=data, headers=headers)
    assert res is not None
    assert res.get('user_string', None) == 'test_mock_1'
    




if __name__ == "__main__":
    pass

    # get jwt
    endpoint = 'api/token/'
    method = 'POST'
    data = {'username': 'test_mock_1', 'password': 'password'}
    token_res = make_request(url=base + endpoint, method=method, data=data)

    print(token_res)



## Try out different requests here

    # data = make_request(base + endpoint, method, headers, data)

    # print(json.dumps(data, indent=4))

    # print('\n---------------------\n')

    # endpoint = 'ok'
    # data = make_request(base + endpoint, method, headers, data)

    # print('\n---------------------\n')

    # endpoint = 'auth_test_one'
    # method = 'POST'
    # data = make_request(base + endpoint, method, headers, data)

    # print(data)
