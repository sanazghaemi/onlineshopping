from django.contrib import admin
from shopping.models import *
# Register your models here.

admin.site.register(Product)
admin.site.register(Feature)
admin.site.register(Review)
admin.site.register(CheckoutDetail)
admin.site.register(OrderItem)
admin.site.register(Order)


