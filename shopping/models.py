from django.db import models
from account.models import UserProfile
from django.urls import reverse
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ImageField(upload_to="images", default="")
    def get_absolute_url(self):
        return reverse("product_view", kwargs={"myid": self.pk})
    
    def __str__(self):
        return self.name

class Feature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    feature = models.CharField(max_length=1000, null=True, blank=True)
 
    def __str__(self):
        return str(self.product) + " Feature: " + self.feature

class Review(models.Model):
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return str(self.customer) +  " Review: " + self.content


class Order(models.Model):
    customer = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100)
 
    def __str__(self):
        return str(self.id)
 
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
 
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
 
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return str(self.order)
 
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
class CheckoutDetail(models.Model):
    customer = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    total_amount = models.CharField(max_length=10, blank=True,null=True)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.address

