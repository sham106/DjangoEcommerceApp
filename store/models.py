from decimal import Clamped
import email
from itertools import product
from unittest.util import _MAX_LENGTH
from urllib import request
from django.db import models
from distutils.command.upload import upload
from django.urls import reverse
from django.contrib.auth.models import User

from django.contrib.auth.hashers import make_password
import uuid



# Create your models here


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,  null=True, blank=True)
    username = models.CharField(max_length=150, null=True)
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=150, null=True)
    birth_date = models.DateField(null=True)
    # password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    inventory = models.IntegerField()
    last_update = models.DateTimeField
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title
# help not to bring an error if there is no image in the field

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
            return url

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[str(self.pk)])



   
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cart_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    completed = models.BooleanField(default=False)

    @property
    def shipping(self):
        shipping = True
        cartitems = self.cartitems_set.all()
        
        return shipping



    @property
    def get_cart_total(self):
        cartitems = self.cartitems_set.all()
        total = sum([item.get_total for item in cartitems])
        return total
    
    @property
    def get_itemtotal(self):
        cartitems = self.cartitems_set.all()
        total = sum([item.quantity for item in cartitems])
        return total

    def __str__(self):
        return str(self.id)        

class Cartitems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product =  models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)


    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total

    

    def __str__(self):
        return self.product.title


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=250, null=False)
    city = models.CharField(max_length=250, null=False)
    state = models.CharField(max_length=250, null=False)
    zipcode = models.CharField(max_length=250, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

