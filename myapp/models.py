from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    fname=models.CharField(max_length=100)
    # lname=models.CharField(max_length=100)
    # DOB=models.DateTimeField(default="",blank=True)
    email=models.EmailField()
    # contact=models.IntegerField()
    password=models.CharField(max_length=100)
    # address=models.CharField(max_length=100)
    usertype=models.CharField(default='buyer',max_length=100)
    

    def __str__(self):
        return self.fname
class Category(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name
class Product(models.Model):
    seller=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    product_name=models.CharField(max_length=100)
    product_price=models.IntegerField()
    product_qty=models.IntegerField()
    product_desc=models.CharField(max_length=500)
    product_image=models.ImageField(upload_to='product_image/')

    def __str__(self):
        return self.product_name+"-"+self.seller.fname

class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.product.product_name+" - "+self.user.fname


class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    date=models.DateTimeField(default=timezone.now)
    product_price=models.IntegerField()
    product_qty=models.IntegerField()
    payment=models.BooleanField(default=False)
    total=models.IntegerField(default=10)
    net_price=models.IntegerField(default=0,null=True,blank=True)
    razorpay_order_id=models.CharField(max_length=100,null=True,blank=True)
    razorpay_payment_id=models.CharField(max_length=100,null=True,blank=True)
    razorpay_payment_signature=models.CharField(max_length=100,null=True,blank=True)


    def __str__(self):
        return self.product.product_name+" - "+self.user.fname