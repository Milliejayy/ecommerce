from django.contrib import admin
from . models import Category, Product, User, Cart, CartItem, Order, OrderItem, ShippingAddress, Payment, Review


# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Payment)
admin.site.register(Review)