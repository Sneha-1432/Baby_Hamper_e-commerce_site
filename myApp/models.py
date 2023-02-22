from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class shopregmodel(models.Model):
    snm = models.CharField(max_length=30)
    sid = models.IntegerField()
    sads = models.CharField(max_length=60)
    semail = models.EmailField()
    sph = models.IntegerField()
    spwd = models.CharField(max_length=20)
    def  __str__(self):
        return self.snm



class pdtupldmodel(models.Model):
    shopid=models.IntegerField()
    pnm = models.CharField(max_length=20)
    prc = models.IntegerField()
    pdtimg = models.ImageField(upload_to='myApp/static')
    dsc = models.CharField(max_length=40)
    def __str__(self):
        return self.pnm



class profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)    #One-To-One
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def  __str__(self):
        return self.user



class cartmodel(models.Model):
    username=models.CharField(max_length=30)
    pnm = models.CharField(max_length=20)
    prc = models.IntegerField()
    pdtimg = models.ImageField()
    dsc = models.CharField(max_length=40)
    def  __str__(self):
        return self.pnm


class wishlistmodel(models.Model):
    username=models.CharField(max_length=30)
    pnm = models.CharField(max_length=20)
    prc = models.IntegerField()
    pdtimg = models.ImageField()
    dsc = models.CharField(max_length=40)
    def  __str__(self):
        return self.pnm



class buymodel(models.Model):
    pnm = models.CharField(max_length=20)
    prc = models.IntegerField()
    pdtimg = models.ImageField()
    dsc = models.CharField(max_length=40)
    qty = models.IntegerField()
    def  __str__(self):
        return self.pnm



class cardpaydetailsmodel(models.Model):
    cardname = models.CharField(max_length=30)
    cardnum = models.CharField(max_length=30)
    cardexpdate = models.CharField(max_length=30)
    securitycode = models.CharField(max_length=40)
    def  __str__(self):
        return self.cardname



class shopnotificationmodel(models.Model):
    content = models.CharField(max_length=200)
    models.DateField(auto_now_add=True)
    def __str__(self):
        return self.content



class usernotificationmodel(models.Model):
    content = models.CharField(max_length=200)
    models.DateField(auto_now_add=True)
    def __str__(self):
        return self.content