from django.contrib import admin
from .models import User, CodeVerification
# Register your models here.

admin.site.register(User),
admin.site.register(CodeVerification),