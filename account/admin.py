from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    readonly_fields=('userid','is_verified','last_login')
# Register your models here.

admin.site.register(User,UserAdmin)
admin.site.register(Profile)
