from django.urls import path
from .views import SignUpView, VerifyCodeApiView, RegisterApiView

urlpatterns=[
    path( 'sign-up/', SignUpView.as_view(), name='signup'),
    path( 'verify-code/', VerifyCodeApiView.as_view(), name='verify'),
    path( 'register/', RegisterApiView.as_view(), name='register'),
]