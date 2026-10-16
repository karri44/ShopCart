from django.contrib import admin
from .models import Order,OrderItem
class ItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product','name','price','quantity']
    can_delete = False
    def has_add_permission(self,request,obj=None): return False
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['reference','user','total','status','created_at']
    list_filter = ['status','created_at']
    readonly_fields = ['reference','user','full_name','email','phone','address','city','postcode','total','payment_method','checkout_token','created_at']
    inlines = [ItemInline]
    def has_add_permission(self,request): return False
    def has_delete_permission(self,request,obj=None): return False
