from .views import index
from django.urls import path
from .views import cart, product_view,checkout,updateItem

urlpatterns = [
    path('',index,name='index'),
    path("product_view/<int:myid>/", product_view, name="product_view"),
    path("cart/",cart, name="cart"),
     path("checkout/", checkout, name="checkout"),
     path('update_item/', updateItem, name="update_item"),

]
