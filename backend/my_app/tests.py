from django.test import LiveServerTestCase
# from django.test.utils import TestCase, Client, 
from .utils.testutils import CustomClient, DbUtil




# Create your tests here.
class BasicTests(LiveServerTestCase):
    
    def setUp(self):
        
        self.myclient = CustomClient(live_server_url=self.live_server_url)
        self.dbutil = DbUtil()
        
        self.seed()
        
    def seed(self):

        self.dbutil.make_user(username='test_user', password='password')
        self.dbutil.make_user(username='user', password='password')
        # self.dbutil.make_user(username='alice', password='password')
        # self.dbutil.make_user(username='bob', password='password')

        self.dbutil.make_tweet(content='lorem ipsum', user_string='user')
        self.dbutil.make_tweet(content='lorem checksum', user_string='test_user')



    def test_so_basic(self):
        
        endpoint = 'auth_test_one'
        method = 'GET'
        res = self.myclient.make_request(endpoint=endpoint,method=method)
        
        self.assertIsNotNone(res)
        
        endpoint = 'auth_test_one'
        method = 'POST'
        res = self.myclient.make_request(endpoint=endpoint,method=method)
        
        self.assertIsNotNone(res)


    def test_basic_login(self):

        endpoint = 'api/token/'
        method = 'POST'
        data = {'username': 'test_user', 'password': 'password'}
        token_res = self.myclient.make_request(
            endpoint=endpoint, method=method, data=data
            )
        self.assertIsNotNone(token_res)
        self.assertIsInstance(token_res.get('access'), str)
        self.assertIsInstance(token_res.get('refresh'), str)

        endpoint = 'auth_test_two'
        protected_res = self.myclient.make_request(
            endpoint=endpoint
            )
        self.assertIsNone(protected_res)
        
        endpoint = 'auth_test_two'
        headers = self.myclient.make_auth_header(token_res['access'])
        protected_res = self.myclient.make_request(
            endpoint=endpoint, headers=headers,
            ) 
        self.assertIsNotNone(protected_res)
        self.assertTrue(protected_res.get('success'))


    def test_login_shared_method(self):

        token_res = self.myclient.get_login_token(username='test_user')
        self.assertIsNotNone(token_res)


    def test_bad_login_1(self):
        
        # login request with wrong password
        endpoint = 'api/token/'
        method = 'POST'
        data = {'username': 'test_user', 'password': 'wrong_password'}
        token_res_obj = self.myclient.make_request(
            endpoint=endpoint, method=method, data=data, return_obj=True
            )
        
        self.assertEqual(token_res_obj.status_code, 401)

        # login request with no empty data object in body
        endpoint = 'api/token/'
        method = 'POST'
        data = {}
        token_res_obj = self.myclient.make_request(
            endpoint=endpoint, method=method, data=data, return_obj=True
            )
        
        self.assertEqual(token_res_obj.status_code, 400)

    def test_new_tweet_is_protected(self):

        # un-authed GET to this route should work
        endpoint = 'tweets/'
        res = self.myclient.make_request(endpoint=endpoint)
        self.assertIsNotNone(res)
        
        # un-authed POST to this route should 401
        endpoint = 'tweets/'
        method = 'POST'
        data = {'username': 'test_mock_1', 'content':'testing command'}
        res = self.myclient.make_request(
            endpoint=endpoint, method=method, data=data
            )
        self.assertIsNone(res)

        # get jwt
        token_res = self.myclient.get_login_token(username='test_user')

        # authed POST should work returning an object
        endpoint = 'tweets/'
        method = 'POST'
        data = {'username':'test_user', 'content':'testing command'}
        headers = self.myclient.make_auth_header(token_res['access'])
        res = self.myclient.make_request(endpoint=endpoint, method=method, data=data, headers=headers)
        self.assertIsNotNone(res)
        self.assertEqual(res.get('user_string'), 'test_user')

    def test_new_tweet_uses_auth_user(self):

        token_res = self.myclient.get_login_token(username='tesT_user')

        # make a new tweet with:
        # auth user: test_user
        # request payload: username: wrong_user
        endpoint = 'tweets/'
        method = 'POST'
        data = {'username': 'wrong_user', 'content':'testing command (wrong user)'}
        headers = self.myclient.make_auth_header(token_res['access'])
        res = self.myclient.make_request(
            endpoint=endpoint, method=method, data=data, headers=headers
            )
        self.assertIsNotNone(res)
        self.assertEqual(res.get('user_string'), 'test_user')


    # def test_hang_test_server(self):
    #     '''
    #         comment this out, unless you want to hang test test server
    #     '''
    #     print('\ntest server hanging...\n')
    #     print(self.client)
    #     print(self.live_server_url)
    #     time.sleep(30)
    #     print('...finished hang test.\n')


if __name__ == '__main__':
    pass
    # client = CustomClient(live_server_url=None)
    # res = client.make_request(endpoint='ok/')
    
    