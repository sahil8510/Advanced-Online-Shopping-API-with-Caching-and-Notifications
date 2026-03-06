from django.contrib import admin
from .models import Category, Product, Order, OrderItem, User
# from rest_framework.authentication


# Register your models here.
class OrderItemInLine(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines=[
        OrderItemInLine
    ]



admin.site.register(Category)   
admin.site.register(Product)   
admin.site.register(Order, OrderAdmin)  
admin.site.register(OrderItem)                                                                          
admin.site.register(User)                                                                          
