from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import *

class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = '__all__'

class AccountAdmin(UserAdmin):
    add_form = UserCreateForm
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name' , 
                  'last_name', 
                  'email',
                  'password' ),
        }),
    )
    
    list_display=('id','first_name','last_name','email','last_login')
    search_fields = ["email","id","first_name"]
    readonly_fields = ['userid',"date_joined","last_login"]
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering =()
    
class WalletAdmin(admin.ModelAdmin):
    list_display=('userid','walletid')
    readonly_fields=('userid','walletid','balance')
# Register your models here.

admin.site.register(User,AccountAdmin)
admin.site.register(Profile)
admin.site.register(Wallet)
