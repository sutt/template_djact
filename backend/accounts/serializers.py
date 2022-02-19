from django.conf import settings
from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.http.response import JsonResponse
from rest_framework.response import Response

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        
        # this can be turned on in proj.settings
        # or can be temporarily enabled by creating a new file and running:
        # python manage.py runserver --settings=my_proj.settings_prime
        try: b_check_password = settings.PASSWORD_VALIDATION_ON
        except: b_check_password = False
        
        if b_check_password:
            print(validated_data)
            try: validate_password(validated_data['password'])
            except Exception as e:
                validation_msg = {'password_validation': e.messages}
                
                # TODO - figure out how to send a custom response
                raise ValidationError(validation_msg)
                # return Response(validation_msg, status=400) #, content_type='application/json')
                

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email',)