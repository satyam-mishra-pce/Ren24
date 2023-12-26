from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display=('id','first_name','last_name','email','last_login')
    readonly_fields=('userid','last_login','is_verified')
    
class WalletAdmin(admin.ModelAdmin):
    list_display=('userid','walletid')
    readonly_fields=('userid','walletid','balance')
# Register your models here.

admin.site.register(User,UserAdmin)
admin.site.register(Profile)
admin.site.register(Wallet)
