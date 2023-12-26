from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    readonly_fields=('userid','is_verified','last_login')
    
class WalletAdmin(admin.ModelAdmin):
    list_display=('userid','walletid')
    readonly_fields=('userid','walletid','balance')
# Register your models here.

admin.site.register(User,UserAdmin)
admin.site.register(Profile)
admin.site.register(Wallet)
