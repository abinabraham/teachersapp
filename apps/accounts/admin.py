from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Subject, \
                    Teacher

#User Admin registration
admin.site.register(User, UserAdmin)

#Subject Admin registration
admin.site.register(Subject)

#Teacher Admin registration
admin.site.register(Teacher)