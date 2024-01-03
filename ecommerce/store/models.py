from django.db import models
from django.contrib.auth.models import User

# clasa Customer, care va servi drept model pentru a stoca informații despre clienți în baza de date.
class Customer(models.Model):
    user  = models.OneToOneField(User,null=True, blank=True, on_delete=models.CASCADE)
    name  = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200)
    

    def __str__(self) :
        return self.name

# Clasa Product, care reprezintă modelele produselor disponibile în magazin.
class Product(models.Model):
    name    = models.CharField(max_length=200)
    price   = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image=models.ImageField(null=True, blank=True)

    def __str__(self) :
        return self.name
    
    @property
    def imageURL(self):
        try :
            url=self.image.url
        except:
            url = ''
        return url

# Clasa Order, care reprezintă comenzile plasate de către clienți.
class Order(models.Model):
    customer       = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered   = models.DateTimeField(auto_now_add=True)
    complete       = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)
    
# Clasa OrderItem, care reprezintă elementele individuale dintr-o comandă.
class OrderItem(models.Model):
    order     = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product   = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity  = models.IntegerField(default=0, null=True, blank=True)
    date_aded = models.DateTimeField(auto_now_add=True)

# Clasa ShippingAddress, care reprezintă adresele de livrare asociate cu comenzile.
class ShippingAddress(models.Model):
    customer  = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order     = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    addrress  = models.CharField(max_length=200, null=False)
    city      = models.CharField(max_length=200, null=False)
    state     = models.CharField(max_length=200, null=False)
    zipcode   = models.CharField(max_length=200, null=False)
    date_aded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.addrress
