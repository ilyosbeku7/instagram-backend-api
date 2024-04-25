from django.shortcuts import render
from .serializers import SignUpSerializer, RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import CodeVerification
from .models import CODE_VERIFIED, NEW, DONE
from datetime import datetime 
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

class SignUpView(APIView):
   
    
    def post(self, request):
        serializer=SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

class VerifyCodeApiView(APIView):
    
    permission_classes=(IsAuthenticated,)
    def post(self, request):
        user=request.user
        if 'code' not in request.data:
            data={
                'status': False,
                "message": "Code field is required"
            }

            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        code=request.data['code']
        print(user)
        result=user.verifications_code.filter(is_verified=False, expiration_time__gte=datetime.now(), code=code).first()

        if result is None:
            data={
                'status': False,
                "message": "Siz kiritgan kod eskirgan yoki xato "
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        token=user.token()

        result.is_verified=True
        result.save()

        if user.auth_status==NEW:

            user.auth_status=CODE_VERIFIED
            user.save()

        data={
            'status':True,
            'message': "Kod muvaffaqiyatli qabul qilindi",
            # 'token':token
        }

        return Response (data, status=status.HTTP_200_OK)

class RegisterApiView(APIView):
    permission_classes=(IsAuthenticated,)
    def put(self, request):
        user=request.user
        serializer=RegisterSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response (serializer.data)
    
class LodinApiView(APIView):
    def post(self, request):
        data=request.data
        serializer=LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        user=authenticate(username=serializer.data['username'],)

        if user is None:
            data={
                'status': False,
                'message': "User not found"
            }
            return Response (data)
        refresh=RefreshToken.for_user(user)

        data={
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
        return Response (data)