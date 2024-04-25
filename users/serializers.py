from rest_framework import serializers
from .models import User
from .regex_check import is_valid_email, is_valid_phone
from .models import VIA_EMAIL, VIA_PHONE
from rest_framework.validators import ValidationError
from .telegram_send_code import send_sms

class SignUpSerializer(serializers.Serializer):
    phone_or_email=serializers.CharField(required=True, write_only=True)

    # def validate_phone_or_email(self, value):
    #     if is_valid_phone(value):
    #         if User.objects.filter(phone_number=value).exists():

    #            data={
    #             'status': False,
    #             'message': "phone number already exists"
    #          }
    #         raise ValidationError(data)

    #     elif is_valid_email(value):
    #         if User.objects.filter(email=value).exists():

    #            data={
    #             'status': False,
    #             'message': "Email already exists"
    #          }
    #         raise ValidationError(data)
    #     return value
        
         
    
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
    
class RegisterSerializer(serializers.ModelSerializer):
    first_name=serializers.CharField(required=True,   min_length=4)
    confirm_password=serializers.CharField(required=True,   min_length=4)

    class Meta:
        model=User
        fields=['username', 'first_name', 'last_name', 'password', 'confirm_password']
    def validate(self, attrs):
        confirm_password=attrs.get('confirm_password')
        password=attrs.get('password')
        username=attrs.get('username')

        if password != confirm_password:
            data={
                    'status': False,
                    'message': "Password don't match",
                } 
        
            raise ValidationError(data)

        if not username.isalpha():
            data={
                    'status': False,
                    'message': "Username faqat harflardan iborat bo'lishi lozim",
                } 
            raise ValidationError(data)
        
    def update(self, instance, validated_data):
            instance.username=validated_data.get('username', instance.username)        
            instance.first_name=validated_data.get('first_name', instance.first_name)        
            instance.last_name=validated_data.get('last_name', instance.last_name)        
            instance.set_password(password=validated_data.get('password') )    
            instance.save()

            return instance  
            