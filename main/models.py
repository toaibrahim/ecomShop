
from time import time
from django.shortcuts import reverse
from django.db import models
from django.contrib.auth.models import User
from .helper import *
from django_countries.fields import CountryField


# Create your models here.

CATEGORY_CHOICES = (
    ('S','Shirt'),
    ('SW','Sports Wear'),
    ('OW','Outwear'),
    ('Cl','Club and Night out'),
    ('PA','Pants'),
)

LABEL_CHOICES = (
    ('N','New'),
    ('B','Bestseller'),
)

PAY_CHOICES = (
    ('C','CashOnDelevery'),
)

class Author(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile = models.ImageField(upload_to = 'profile',null=True,blank=True)

    def __str__(self):
        return self.user.username

class Item(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    specification = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to="itemImage",null=True,blank=True)
    price = models.FloatField()
    discount_price = models.FloatField(null=True,blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2,default='None')
    label = models.CharField(choices=LABEL_CHOICES,max_length=2,null=True,blank=True)
    slug = models.SlugField(null=True,blank=True)
    featured = models.BooleanField(default=False) 
    time = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        self.slug = generate_slug(self.title)
        super(Item,self).save(*args,**kwargs)


    def short_des(self):
        return self.description[0:40]
    
    

    def get_absolute_url(self):
        return reverse("main:product_details",kwargs={
            'slug':self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("main:add_to_cart",kwargs={
            'slug':self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("main:remove_from_cart",kwargs={
            'slug':self.slug
        })
    
    def get_add_to_wishlist_url(self):
        return reverse("main:add_to_wishlist",kwargs={
            'slug':self.slug
        })

    def get_remove_from_wishlist_url(self):
        return reverse("main:remove_from_wishlist",kwargs={
            'slug':self.slug
        })


    @property
    def get_comments(self):
        return self.comments.all()

    @property
    def count_comment(self):
        return Reviews.objects.filter(product=self).count()


class ImageGallery(models.Model):
    product = models.ForeignKey(Item,on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    gallery = models.ImageField()

    def __str__(self):
        return str(self.product.title)


class OrderItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,default=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def total_price(self):
        return self.item.price*self.quantity


    def total_discount_price(self):
        return self.item.discount_price*self.quantity

    def get_final_total(self):
        if self.item.discount_price:
            return self.total_discount_price()
        else:
            return self.total_price()



    def get_absolute_url(self):
        return reverse("main:product_details",kwargs={
            'slug':self.item.slug
        })

    def get_add_to_cart_url(self):
        return reverse("main:add_to_cart",kwargs={
            'slug':self.item.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("main:remove_from_cart_totally",kwargs={
            'slug':self.item.slug
        })

    def get_remove_from_cart_byone_url(self):
        return reverse("main:remove_from_cart",kwargs={
            'slug':self.item.slug
        })


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress',on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return f'{self.user.username} has ordered'

    def get_all_total(self):
        total = 0
        for add in self.items.all():
            total += add.get_final_total()

        return total

    def get_absolute_url(self):
        return reverse("main:product_details",kwargs={
            'slug':self.item.slug
        })


    
class WishlistItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    wishlist = models.BooleanField(default=False)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)

    def __str__(self):
        return self.item.title

    def get_absolute_url(self):
        return reverse("main:product_details",kwargs={
            'slug':self.item.slug
        })

    def get_add_to_cart_url(self):
        return reverse("main:add_to_cart",kwargs={
            'slug':self.item.slug
        })

    def get_add_to_wishlist_url(self):
        return reverse("main:add_to_wishlist",kwargs={
            'slug':self.item.slug
        })

    def get_remove_from_wishlist_url(self):
        return reverse("main:remove_from_wishlist",kwargs={
            'slug':self.item.slug
        })

class Wishlisted(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Wishlist = models.BooleanField(default=False)
    items = models.ManyToManyField(WishlistItem)
    start_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class BillingAddress(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    email = models.EmailField()
    mobile = models.IntegerField()
    address = models.CharField(max_length=1000)
    country = CountryField(multiple = True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    payment_option = models.CharField(choices=PAY_CHOICES,default=None,max_length=2)
    
    

    def __str__(self):
        return self.user.username



class Reviews(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Item,related_name='comments',on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField(max_length=500)
    rate = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} rated {self.rate}'


class BlogPost(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=10000)
    photo = models.ImageField(upload_to = 'blogimage', null = True,blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def des_snipet(self):
        return self.description[0:200]

    

    def get_absolute_blog_url(self):
        return reverse("main:blog_details",kwargs={
            'id':self.id
        })
