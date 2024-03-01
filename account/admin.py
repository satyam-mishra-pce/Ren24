from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.sessions.models import Session
from import_export.admin import ExportActionMixin,ExportActionModelAdmin,ImportExportMixin
from .models import *

class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email','password']
        

class AccountAdmin(ExportActionMixin,UserAdmin):
    # add_form = UserCreateForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                  'email',
                  'password1',
                  'password2' 
                  ),
        }),
    )
    
    list_display=('id','first_name','last_name','email','last_login')
    search_fields = ["email","id","first_name"]
    readonly_fields = ['id',"date_joined","last_login"]
    autocomplete_fields = ["_pass"]
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering =()
    
class PassAdmin(ImportExportMixin,admin.ModelAdmin):
    empty_value_display = "Not selected"
    list_display=['psid','email','technical','splash']
    readonly_fields=['technical','splash']
    search_fields = ['email']


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
    
class ProfileAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display = ['get_email','get_name','phone']
    autocomplete_fields = ["user"]
    
    def get_email(self,obj):
        return obj.user.email 
    
    def get_name(self,obj):
        return f'{obj.user.first_name} {obj.user.last_name}'
    get_email.short_description = "Email"
    get_email.admin_order_field = "user__email"
    get_name.short_description = "Name"
    get_name.admin_order_field = "user__first_name"

admin.site.register(Session, SessionAdmin)
admin.site.register(User,AccountAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Passes,PassAdmin)
admin.site.register(OTP)
# admin.site.register(Wallet,WalletAdmin)
