from django.contrib import admin
from .models import *
from import_export.admin import ExportActionMixin
from config.settings import BASE_URL
# Register your models here.

class EventAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display=('name','type','amount','date','time')
    
class TicketAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display=('get_username','get_link' ,'get_email','get_price','get_date')
    
    def get_date(self,obj):
        return f"{obj.event.date} {obj.event.time}" 
    
    def get_price(self,obj):
        return obj.event.amount 
    
    def get_email(self,obj):
        return obj.user.email 
    
    def get_username(self,obj):
        return f'{obj.user.first_name} {obj.user.last_name}'
    
    def get_link(self,obj):
        return f"{BASE_URL}/qr/{obj.id}" 
    get_link.short_description = "Link"
    
    get_date.short_description = "Date & Time"
    get_date.admin_order_field = "events__date"
    get_price.short_description = "Price"
    get_price.admin_order_field = "events__cost"
    get_email.short_description = "Email"
    # get_email.admin_order_field = "user__email"
    get_username.short_description = "Name"
    get_username.admin_order_field = "user__first_name"
    
    
# class CustomTicketAdmin(ExportActionMixin,admin.ModelAdmin):
#     list_display = ['get_link','event','amount','comment']
#     readonly_fields = ['user','date','is_paid']
#     fieldsets = (
#         (None, {
#             'fields': ['event','amount'],
#             'description': f"This will generate a custom ticket for the selected event & amount, The form can be accessed from the link on display"
#         }),
#         (None, {
#             'fields': ['user','date','is_paid'],
#             }),
#     )
#     def get_link(self,obj):
#         return f"{BASE_URL}/custom/{obj.id}" 
#     get_link.short_description = "Link"


admin.site.register(Events,EventAdmin)
admin.site.register(Ticket,TicketAdmin)
admin.site.register(CustomTicket)
# admin.site.register(CustomTicket,CustomTicketAdmin)