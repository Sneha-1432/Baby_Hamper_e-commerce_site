from django import forms

class shopregform(forms.Form):
    sname=forms.CharField(max_length=30)
    sid=forms.IntegerField()
    sadrs=forms.CharField(max_length=60)
    semail=forms.EmailField()
    sphn=forms.IntegerField()
    spswd=forms.CharField(max_length=20)
    cpswd=forms.CharField(max_length=20)



class shoploginform(forms.Form):
    sname=forms.CharField(max_length=30)
    spswd=forms.CharField(max_length=30)



class pdtuploadforms(forms.Form):
    pname=forms.CharField(max_length=20)
    price=forms.IntegerField()
    pdtimg=forms.ImageField()
    desc=forms.CharField(max_length=40)



class cardpaydetailsform(forms.Form):
    cardname=forms.CharField(max_length=30)
    cardnum=forms.CharField(max_length=30)
    cardexpdate=forms.CharField(max_length=30)
    securitycode=forms.CharField(max_length=40)