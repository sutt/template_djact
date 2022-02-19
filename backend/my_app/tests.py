from django.test import LiveServerTestCase
from django.test import override_settings
from django.conf import settings
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

        token_res = self.myclient.get_login_token(username='test_user')

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


    def test_new_signup_1(self):
        '''
            basic signup with "common" password
            use login request to verfiy the signup worked
        '''

        # signup request
        endpoint = 'api/auth/signup/'
        method = 'POST'
        data = {
            'username':'signup_user_1',
            'password':'password',
            'email':'test_user_1@email.com',
        }
        signup_res = self.myclient.make_request(
            endpoint=endpoint, method=method, data=data,
        )
        
        # test signup
        self.assertIsNotNone(signup_res)

        # use signup credentials to login
        token_res = self.myclient.get_login_token(
            username='signup_user_1',
            password='password'
        )
        # verify login worked
        self.assertIsNotNone(token_res)


    def test_new_signup_2(self):
        '''
            simple signup with "common" password
            use orm to verify the signup user is added to db
            use orm to verify `password` field not readable in serialization of `User`
        '''

        # sign up request
        endpoint = 'api/auth/signup/'
        method = 'POST'
        data = {
            'username':'signup_user_1',
            'password':'password',
            'email':'test_user_1@email.com',
        }
        signup_res = self.myclient.make_request(
            endpoint=endpoint, method=method, data=data,
        )
        
        # verfiy signup worked via response
        self.assertIsNotNone(signup_res)
        self.assertEqual(signup_res.get('username'), 'signup_user_1')

        # verfiy signup worked via orm
        bool_found_user = self.dbutil.check_for_user('signup_user_1')
        self.assertTrue(bool_found_user)


    def test_bad_signup_1(self):
        '''
            check response when sent with no-password/no-username
        '''
        # sign up request, no username
        endpoint = 'api/auth/signup/'
        method = 'POST'
        data = {
            'username':'',
            'password':'password',
            'email':'test_user_1@email.com',
        }
        res_obj = self.myclient.make_request(
            endpoint=endpoint, method=method, data=data, return_obj=True
        )

        self.assertEqual(res_obj.status_code, 400)
        
        res_dict = res_obj.json()
        self.assertTrue(
            'This field may not be blank.' in res_dict.get('username')
            )

        # sign up request, no password
        endpoint = 'api/auth/signup/'
        method = 'POST'
        data = {
            'username':'valid_user',
            'password':'',
            'email':'test_user_1@email.com',
        }
        res_obj = self.myclient.make_request(
            endpoint=endpoint, method=method, data=data, return_obj=True
        )

        self.assertEqual(res_obj.status_code, 400)
        
        res_dict = res_obj.json()
        self.assertTrue(
            'This field may not be blank.' in res_dict.get('password')
            )


    def test_duplicate_user_signup(self):
        '''
            test that two users can't signup with same `username`
            test that the response is a 400 with the message we expect
        '''

        # first user, signup should work
        endpoint = 'api/auth/signup/'
        method = 'POST'
        data = {
            'username':'duplicate_user',
            'password':'password1',
            'email':'dup1@email.com',
        }
        signup_res = self.myclient.make_request(
            endpoint=endpoint, method=method, data=data,
        )
        self.assertIsNotNone(signup_res)

        # second time, same user, diff password, diff email
        endpoint = 'api/auth/signup/'
        method = 'POST'
        data = {
            'username':'duplicate_user',
            'password':'password2',
            'email':'dup2@email.com',
        }
        res_obj = self.myclient.make_request(
            endpoint=endpoint, method=method, data=data, return_obj=True,
        )

        # test for proper characteristics of duplicate user response
        self.assertEqual(res_obj.status_code, 400)
        
        res_dict = res_obj.json()
        self.assertTrue(
            'A user with that username already exists.' in res_dict.get('username')
            )
        

    def test_password_checker_on_1(self):
        '''
            check if password validators can be turned on and accept/reject appropriately
            note: they are turned off by default, but we can override that in this test
        '''
        self.assertFalse(settings.PASSWORD_VALIDATION_ON)
        
        with override_settings(PASSWORD_VALIDATION_ON = True):
            
            # verify we're running with the password validation turned on
            self.assertTrue(settings.PASSWORD_VALIDATION_ON)

            # signup with unacceptable password (too common)
            endpoint = 'api/auth/signup/'
            method = 'POST'
            data = {
                'username':'validation_user',
                'password':'password',
                'email':'user@email.com',
            }
            signup_res = self.myclient.make_request(
                endpoint=endpoint, method=method, data=data,
            )
            
            # verify common password gets rejected
            self.assertIsNone(signup_res)


            # signup with acceptable password
            endpoint = 'api/auth/signup/'
            method = 'POST'
            data = {
                'username':'validation_user',
                'password':'eXjf987sj23',
                'email':'user@email.com',
            }
            signup_res = self.myclient.make_request(
                endpoint=endpoint, method=method, data=data,
            )
            
            # verify strong password allows us to signup
            self.assertIsNotNone(signup_res)




    def test_password_checker_on_2(self):
        '''
            check if password validators can be and have correct error message
            note: they are turned off by default, but we can override that in this test
        '''
        self.assertFalse(settings.PASSWORD_VALIDATION_ON)
        
        with override_settings(PASSWORD_VALIDATION_ON = True):
            
            self.assertTrue(settings.PASSWORD_VALIDATION_ON)

            # TODO - figure out how to send custom responses from:
            #        accounts.serializers.UserSerializer.create
            
            # TOO_SHORT = 'This password is too short. It must contain at least 8 characters.',
            # TOO_COMMON = 'This password is too common.'
            # MSG_KEY = 'password_validation'

            # # check common password
            # endpoint = 'api/auth/signup/'
            # method = 'POST'
            # data = {
            #     'username':'validation_user',
            #     'password':'password',         # too common password
            #     'email':'validation_user@email.com',
            # }
            # res_obj = self.myclient.make_request(
            #     endpoint=endpoint, method=method, data=data, return_obj=True
            # )
            # self.assertEqual(res_obj.status_code, 400)
            # msg_dict = res_obj.json()
            # self.assertTrue(TOO_COMMON in msg_dict[MSG_KEY])
            # self.assertTrue(TOO_SHORT not in msg_dict[MSG_KEY])

            # # check too short password
            # endpoint = 'api/auth/signup/'
            # method = 'POST'
            # data = {
            #     'username':'validation_user',
            #     'password':'ex9',               # too short password
            #     'email':'validation_user@email.com',
            # }
            # res_obj = self.myclient.make_request(
            #     endpoint=endpoint, method=method, data=data, return_obj=True
            # )
            # self.assertEqual(res_obj.status_code, 400)
            # msg_dict = res_obj.json()
            # self.assertTrue(TOO_SHORT in msg_dict[MSG_KEY])
            # self.assertTrue(TOO_COMMON not in msg_dict[MSG_KEY])

            # # check common + too short
            # endpoint = 'api/auth/signup/'
            # method = 'POST'
            # data = {
            #     'username':'validation_user',
            #     'password':'user',              # too short and too common password
            #     'email':'validation_user@email.com',
            # }
            # res_obj = self.myclient.make_request(
            #     endpoint=endpoint, method=method, data=data, return_obj=True
            # )
            # self.assertEqual(res_obj.status_code, 400)
            # msg_dict = res_obj.json()
            # self.assertTrue(TOO_SHORT in msg_dict[MSG_KEY])
            # self.assertTrue(TOO_COMMON in msg_dict[MSG_KEY])






    # def test_hang_test_server(self):
    #     '''
    #         comment this out, unless you want to hang test test server
    #     '''
    #     print('\ntest server hanging...\n')
    #     print(self.client)
    #     print(self.live_server_url)
    #     import time
    #     time.sleep(30)
    #     print('...finished hang test.\n')


if __name__ == '__main__':
    pass
    # client = CustomClient(live_server_url=None)
    # res = client.make_request(endpoint='ok/')
    
    