

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
