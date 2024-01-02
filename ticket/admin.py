from django.contrib import admin
from .models import *
# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display=('name','type','cost','date','time')
    
class TicketAdmin(admin.ModelAdmin):
    list_display=('get_username','get_email','get_price','get_date')
    
    def get_date(self,obj):
        return f"{obj.event.date} {obj.event.time}" 
    
    def get_price(self,obj):
        return obj.event.cost 
    
    def get_email(self,obj):
        return obj.user.email 
    
    def get_username(self,obj):
        return f'{obj.user.first_name} {obj.user.last_name}'
    
    get_date.short_description = "Date & Time"
    get_date.admin_order_field = "event__date"
    get_price.short_description = "Price"
    get_price.admin_order_field = "event__cost"
    get_email.short_description = "Email"
    get_email.admin_order_field = "user__email"
    get_username.short_description = "Name"
    get_username.admin_order_field = "user__first_name"
    

admin.site.register(RazorpayPayments)
admin.site.register(Event,EventAdmin)
admin.site.register(Ticket,TicketAdmin)