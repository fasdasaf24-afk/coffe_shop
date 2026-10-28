from django.contrib import admin
from .models import Product, Location, Operator, Order, SupportMessage, Review

admin.site.register(Product)
admin.site.register(Location)
admin.site.register(Operator)
admin.site.register(Order)
admin.site.register(SupportMessage)
admin.site.register(Review)
