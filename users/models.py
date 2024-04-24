
import random
import uuid
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken



VIA_EMAIL, VIA_PHONE = ("via_email", "via_phone")
NEW, CODE_VERIFIED, DONE, PHOTO_DONE = ('new', 'code_verified', 'done', 'photo_done')


class User(AbstractUser):
   
    AUTH_TYPE = (
        (VIA_PHONE, VIA_PHONE),
        (VIA_EMAIL, VIA_EMAIL)
    )
    AUTH_STEP= (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
        (DONE, DONE),
        (PHOTO_DONE, PHOTO_DONE)
    )

    bio=models.TextField()
    auth_type = models.CharField(max_length=31, choices=AUTH_TYPE)
    auth_status = models.CharField(max_length=31, choices=AUTH_STEP, default=NEW)
    phone_number = models.CharField(max_length=13, null=True, blank=True, unique=True)
    photo = models.ImageField(upload_to='user_photos/', default='users/default.jpg' )

    def __str__(self):
        return self.username
   

    def check_username(self):
        if not self.username:
            temp_username = f'instagram-{uuid.uuid4().__str__().split("-")[-1]}' 
            while User.objects.filter(username=temp_username):
                temp_username = f"{temp_username}{random.randint(0,9)}"
            self.username = temp_username


    def clean_password(self):
        if not self.password:
            self.password = f'instagram-{uuid.uuid4().__str__().split("-")[-1]}' 
           

    def hashing_password(self):
        if not self.password.startswith('pbkdf2_'):
            self.set_password(self.password)

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh_token": str(refresh)
        }

    def save(self, *args, **kwargs):
        self.clean()
        super(User, self).save(*args, **kwargs)

    def clean(self):
        self.check_username()
        self.clean_password()
        self.hashing_password()

    def create_code(self, auth_type):
        code = "".join([  str (random.randint( 0,  9)) for _ in range(5)])

        CodeVerification.objects.create(
            auth_type=auth_type,
            code=code,
            user=self
            )
        return code


class CodeVerification(models.Model):
    AUTH_TYPE = (
        (VIA_PHONE, VIA_PHONE),
        (VIA_EMAIL, VIA_EMAIL)
    )
    code = models.CharField(max_length=5)
    auth_type = models.CharField(max_length=31, choices=AUTH_TYPE)
    user = models.ForeignKey('users.User', models.CASCADE, related_name='verify_codes')
    expiration_time = models.DateTimeField(null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.__str__())

    def save(self, *args, **kwargs):
        if self.auth_type == VIA_EMAIL: 
            self.expiration_time = datetime.now() + timedelta(minutes=2)
        else:
            self.expiration_time = datetime.now() + timedelta(minutes=2)
        super(CodeVerification, self).save(*args, **kwargs)