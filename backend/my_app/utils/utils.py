import datetime
import time


def token_analytics(auth):

    auth_payload = auth.payload

    iss_timestamp = auth.payload['iat']
    exp_timestamp = auth.payload['exp']
    
    iss = datetime.datetime.fromtimestamp(iss_timestamp)
    exp = datetime.datetime.fromtimestamp(exp_timestamp)

    now = datetime.datetime.now()

    is_valid = now < exp

    diff_exp_now_secs = (exp - now).seconds

    data = {
        'iss_timestamp' : iss_timestamp,
        'exp_timestamp' : exp_timestamp,
        'iss'           : iss.ctime(),
        'exp'           : exp.ctime(),
        'server_now'    : now.ctime(),
        'is_valid'      : is_valid,
        'diff_exp_now_secs' : diff_exp_now_secs,

    }

    return data
    




def  print_properties(request_obj=None, view_class=None):
    try:
        if request_obj is not None:
        
            print('request.user.is_authenticated -----')
            print(request_obj.user.is_authenticated)
            print('request.user -----')
            print(request_obj.user)
            print('request.auth -----')
            print(request_obj.auth)
            print('dir(request.auth) -----')
            print(dir(request_obj.auth))
        
        if view_class is not None:
            print('view_class.permission_classes------')
            print(view_class.permission_classes)
            print('view_class.authentication_classes------')
            print(view_class.authentication_classes)


    except Exception as e:
        print(f'`utils.print_properties exception on:\n{e}')
