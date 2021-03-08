from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):

    title = models.CharField(max_length=256)
    price = models.FloatField(default=0)
    description = models.CharField(max_length=256,default="Description (Required)")
    link = models.CharField(max_length=256,blank=True)
    status = models.BooleanField(default=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name="author")
    MY_CHOICES = (
        ('Toys', 'Toys'),
        ('Cars', 'Cars'),
        ('Fashion', 'Fashion'),
        ('House', 'House'),
        ('None', 'None')
    )
    category = models.CharField(max_length=10, choices=MY_CHOICES,default="None")

    def __str__(self):
        return f"{self.title},{self.price},{self.description},{self.link},{self.status},{self.category},{self.author.username}"

class Comments(models.Model):

    comment = models.CharField(max_length=256)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="com")

    def __str__(self):
        return f"{self.comment},{self.listing}"

class Bids(models.Model):

    bid = models.FloatField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name="bid_author")

    def __str__(self):
        return f"{self.bid},{self.listing.title},{self.author.username}"
    


class Watchlist(models.Model):
    
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.listing.title},{self.user.username}"
    