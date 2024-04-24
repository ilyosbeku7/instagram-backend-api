from rest_framework import serializers
from .models import User
from .regex_check import is_valid_email, is_valid_phone
from .models import VIA_EMAIL, VIA_PHONE
from rest_framework.validators import ValidationError
from .telegram_send_code import send_sms

class SignUpSerializer(serializers.Serializer):
    phone_or_email=serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        phone_or_email=attrs.get('phone_or_email')
        if is_valid_phone:
            auth_type=VIA_PHONE

        elif is_valid_email(phone_or_email):
            auth_type=VIA_EMAIL
        
        else:  
            data={
                'status': False,
                'message': "Enter a valid email or phone number"
            }

            raise ValidationError(data)
        
        attrs['auth_type']=auth_type
        return attrs

    def create(self, validated_data):
        phone_or_email = validated_data['phone_or_email']
        auth_type = validated_data['auth_type']

        if is_valid_phone(phone_or_email):
            user=User.objects.create(auth_type=auth_type)
            code=user.create_code(auth_type)
            send_sms(code)
        else:
            user=User.objects.create(auth_type=auth_type)
            code= user.create_code(auth_type)  
            send_sms(code)
        
        validated_data['user']=user

        return validated_data
    
    def to_representation(self, instance):
        user=instance['user']
        data={
            'status': True,
            'message': "Code send your contact",
            'tokens': user.token()
        }
        return data