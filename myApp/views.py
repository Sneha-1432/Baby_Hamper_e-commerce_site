from django.contrib.auth import authenticate
from django.core.mail import send_mail
from Baby_Hamper.settings import EMAIL_HOST_USER
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from .models import *
import os
from django.contrib.auth.models import User
import uuid
from django.contrib import messages
import datetime
from datetime import timedelta

# Create your views here.

def homepg(request):
    return render(request,'homepg.html')



def index(request):
     return render(request,'index.html')



def shopereg(request):
     if request.method=="POST":
         a=shopregform(request.POST)
         if a.is_valid():
             nm = a.cleaned_data["sname"]
             id = a.cleaned_data["sid"]
             adrs=a.cleaned_data["sadrs"]
             email=a.cleaned_data["semail"]
             phn=a.cleaned_data["sphn"]
             pwd=a.cleaned_data["spswd"]
             cpwd=a.cleaned_data["cpswd"]
             if pwd==cpwd:
                 b=shopregmodel(snm=nm, sid=id, sads=adrs, semail=email, sph=phn, spwd=pwd)
                 b.save()
                 return redirect(shoplogin)   #redirect() fn is used to redirect into an other FUNCTION or URL, import redirect
             else:
                 return HttpResponse("password doesn't match")
         else:
             return HttpResponse("Registration Failed")
     return render(request, 'register_shop.html')



def shoplogin(request):
    if request.method=="POST":
        a=shoploginform(request.POST)
        if a.is_valid():
            nm=a.cleaned_data['sname']
            pwd=a.cleaned_data['spswd']
            b=shopregmodel.objects.all()
            # to make a variable global {we want to get this shop name on shop profile page. we need to access this snmae on other func(we need to send this shop name which we will get while login,to shop profile func)}
            request.session['shopnm']=nm     #shopnm is just a vailable we use to store shopname
            for i in b:
                if nm==i.snm and pwd==i.spwd:
                    request.session['sid']=i.id
                    return redirect(shopprofile)
            else:
                return HttpResponse("Login Failed")
    return render(request, 'login_shop.html')



def shopprofile(request):
    shopname=request.session['shopnm']
    return render(request,'shop_profile.html', {'shopname':shopname})



def uploadpdt(request):
    if request.method=="POST":
        a=pdtuploadforms(request.POST, request.FILES)
        id=request.session['sid']
        if a.is_valid():
            pn=a.cleaned_data['pname']
            pr=a.cleaned_data['price']
            pimg=a.cleaned_data['pdtimg']
            pd=a.cleaned_data['desc']
            b=pdtupldmodel(shopid=id,pnm=pn,prc=pr,pdtimg=pimg,dsc=pd)
            b.save()
            return redirect(pdtdisplay)
        else:
            return HttpResponse("Pdt uploading failed")
    return render(request, 'pdt_upload.html')



def pdtdisplay(request):              #func to view their pdts only
    shpid=request.session['sid']
    a=pdtupldmodel.objects.all()
    pname=[]
    price=[]
    pdtimg=[]
    desc=[]
    id=[]
    shopid=[]
    for i in a:
        sid=i.shopid
        shopid.append(sid)
        pn=i.pnm
        pname.append(pn)
        prc=i.prc
        price.append(prc)
        img=i.pdtimg
        pdtimg.append(str(img).split('/')[-1])
        ds=i.dsc
        desc.append(ds)
        pid=i.id
        id.append(pid)
        mylist=zip(pname,price,pdtimg,desc,id,shopid)
    return render(request, 'pdt_display.html',{'pdtdata':mylist,'shpid':shpid})



def pdtdelete(request,id):
    a=pdtupldmodel.objects.get(id=id)
    a.delete()
    return redirect(pdtdisplay)



def pdtedit(request,id):
    a=pdtupldmodel.objects.get(id=id)       #a=id,imgname,desc,image,price
    img=str(a.pdtimg).split('/')[-1]         # passing the image of product to display. split the path of img in order to get the image path only as we do for other images
    if request.method=='POST':
        if len(request.FILES):              #image field editing- FILE field l(ie, image field, {img, adio, vdo etc are passed under 'FILES'}) nte length nokunnu, ie, FILES method vazhi vere image vannitundo nn nokum(ie, the length of FILES)
            if len(a.pdtimg)>0:             #old image avide undo nn nokum... (Old file)
                os.remove(a.pdtimg.path)     #if there is old image exists in that field(table field), then we will remove that old img with the help of 'os',, as the images are stored in an encrypted form , we should need 'os' to remove that path
            a.pdtimg=request.FILES['image']
        a.pnm=request.POST.get('pname')
        a.prc=request.POST.get('price')
        a.dsc=request.POST.get('desc')
        a.save()
        return redirect(pdtdisplay)
    return render(request, 'edit_pdt.html',{'a':a,'im':img})




def view_all_shoppdts(request):
    a = pdtupldmodel.objects.all()
    pname = []
    price = []
    pdtimg = []
    desc = []
    id = []
    # shopid = []
    for i in a:
        # sid = i.shopid
        # shopid.append(sid)
        pn = i.pnm
        pname.append(pn)
        prc = i.prc
        price.append(prc)
        img = i.pdtimg
        pdtimg.append(str(img).split('/')[-1])
        ds = i.dsc
        desc.append(ds)
        pid = i.id
        id.append(pid)
        mylist = zip(pname, price, pdtimg, desc, id)
    return render(request, 'view_all_pdts_shop.html', {'pdtdata': mylist})



def custreg(request):
    if request.method=='POST':
        unm=request.POST.get('uname')     # here we are not using forms.py.  the line means that request chytha HTML page le POST method vazhi pass cheyth vanna data le 'uname'  enn name ulla data ne directly HTML pg nn get cheyth 'username' nn paaryunna variable lottu save cheyuka.
        fnm=request.POST.get('fname')
        lnm=request.POST.get('lname')
        eml=request.POST.get('uemail')
        pwd=request.POST.get('pswd')

        if User.objects.filter(username=unm).first():  # here we are checking whether the user name already exist..... filter() fn is is used to filter our search and allows yoou to return only the rows that matches the search condition(term).... first() fn-- filter chyth kazhiyumbol condition match chyunna objects nte oru row kitum... first() fn athil ninn first object(which has high match to the condition) ne get cheyikumm........... the if condition checks that, angane name matching aytulla orale kitiyitund enkil, message.success() nn parayunna oru in-built fn work cheyanam
            messages.success(request, 'username already taken')
            return redirect(custreg)
        if User.objects.filter(email=eml).first():
            messages.success(request, 'email already exist')
            return redirect(custreg)
        #if both conditions fails,,, ie, if it's a new user, then do the following
        user_obj=User(username=unm, email=eml, first_name=fnm, last_name=lnm)        #user_obj is a varibale to store the model 'User'.... ||   ith oru new user anh enkil 'User' nn parayunna built-in model nte 'username' field lottu unm variable l ulla value store cheya, last_name field lottu lnm l ulla name um, etc...
        user_obj.set_password(pwd)         #set_password is fn used to secure our pswd...  This fn is called seperately to store password.
        user_obj.save()
        #the following are stored on another module: module Profile
        #token generating-- import uuid module- uuid stands for univerasaly unique identifiers--- uuid model provides 4 fns, we use the fn 'uuid4'
        auth_tkn = str(uuid.uuid4())   #the token is stored as a sting in DB. so convert the token into string using str() fn--- ex of token:vd3fr5476h98hj7dfg898h87u99
        profile_obj = profile.objects.create(user=user_obj, auth_token=auth_tkn)   # 'User' model l ulla ela data yum user_obj vazhi 'profile' model lottu pass chythu---ie. one to one connection
        profile_obj.save()
        send_mail_reg(eml, auth_tkn)     #it's a user defined fn for sending mail, here we send the the mail along with the token number
        return render(request, 'success.html')
    return render(request, 'register_user.html')



def send_mail_reg(email,auth_token):
    subject = "your account has been verified"
    message = f'click the link to verify your account http://127.0.0.1:8000/myApp/verify/{auth_token}'
    email_from= EMAIL_HOST_USER     #from
    recipient = [email]  #to
    send_mail(subject,message,email_from, recipient)        # send_mail()--- is a built-in func in django. basically we pass 4 things to this func : send_mail(subject, message, from_mail, recipient_list)




def verify(request, auth_token):    #token:abc123bcd2
    profile_obj= profile.objects.filter(auth_token=auth_token).first()  # profile nn parayunna model le auth_token=auth_token(pass chyth kitiya token id) aayt match ulla objects ne filter chyth edukum. it will return a row of objects from that object we select the first one using first() func
    if profile_obj:  # true(if it found such a user with that token id which is passed to this func)
        if profile_obj.is_verified:    # if profile_object false(if it's already verified, if he has already clicked on that varification link )
            messages.success(request, "your account is already verified")  # this msg will be passed to the front end
            return redirect(user_login)
        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request, 'your account has been verified')
        return redirect(user_login)
    else:
        messages.success(request, 'user not found')
        return redirect(user_login)



def user_login(request):
    if request.method=='POST':
        username=request.POST.get('uname')    # nyrah
        password=request.POST.get('pswd')        #123
        request.session['uname']=username   #username globally declared
        user_obj=User.objects.filter(username=username).first()
        #user_obj=nyrah
        if user_obj is None:   #user doesn't exist
            messages.success(request, 'user not found')
            return redirect(user_login)
        #first 'User' nn parayunna model l check chyum whether this user exists or not, then next  model aaytulla 'profile' l nammal check cheyum. ath anh following lines l koduthekunne
        #user_obj=nyrah
        profile_obj=profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified: #if profile is not verified(means that, ath true state l allenkil.. do the next step) ----- is_verified is set as 'false' by default, if not means, if it is not in true state
            messages.success(request, 'profile not verified, please check your mail')
            return redirect(user_login)
        # if user exists--- ie,if uname is correct and the user account is verified then he can login, login chyan aayt 'authenticate' nn parayunna func lottu we will pass the credentials do
        user = authenticate(username=username, password=password)  #authenticate() func lotu uname and pswd pass chyum... aa func ee credentials valid ano nn nokum(both unmae and pswd), if it is valid, then that func will return a user object
        if user is None:  # if authenticate() func doesn't return anything, ie, the credentials passed is wrong or if there is not such a user, then,
            messages.success(request,'wrong password or username')
            return redirect(user_login)
        #if authentication is success, then
        return redirect(user_profile)
    return render(request, 'login_user.html')

def user_profile(request):
    usernm = request.session['uname']
    return render(request,'user_profile.html',{'username':usernm})


def user_view_pdt(request):
    a = pdtupldmodel.objects.all()
    pname = []
    price = []
    pdtimg = []
    desc = []
    id = []
    for i in a:
        pn = i.pnm
        pname.append(pn)
        prc = i.prc
        price.append(prc)
        img = i.pdtimg
        pdtimg.append(str(img).split('/')[-1])
        ds = i.dsc
        desc.append(ds)
        pid = i.id
        id.append(pid)
        mylist = zip(pname, price, pdtimg, desc, id)
    return render(request, 'user_viewpdt.html', {'pdtdata': mylist})



def addtocart(request,id):
    usernm = request.session['uname']
    a= pdtupldmodel.objects.get(id=id)    #pdtupldmodel nn particular id ulla object nte data eduthu variable 'a' lottu store chythu
    b=cartmodel(username=usernm,pnm=a.pnm, prc=a.prc,pdtimg=a.pdtimg,dsc=a.dsc)    #cartmodel le fields lotu data store chyunnu.
    b.save()
    return HttpResponse("item added to your cart successfully")



def addtowishlist(request,id):
    usernm = request.session['uname']
    a=pdtupldmodel.objects.get(id=id)
    b=wishlistmodel(username=usernm,pnm=a.pnm, prc=a.prc, pdtimg=a.pdtimg, dsc=a.dsc)
    b.save()
    return HttpResponse("item added to your Wishlist")



def wishlistdisplay(request):
    usernm = request.session['uname']
    a=wishlistmodel.objects.all()
    username = []
    pname = []
    price = []
    pdtimg = []
    desc = []
    id = []
    for i in a:
        uname=i.username
        username.append(uname)
        pn = i.pnm
        pname.append(pn)
        prc = i.prc
        price.append(prc)
        img = i.pdtimg
        pdtimg.append(str(img).split('/')[-1])
        ds = i.dsc
        desc.append(ds)
        pid = i.id
        id.append(pid)
        mylist = zip(pname, price, pdtimg, desc, id, username)
        print(pname,price,desc,pdtimg,id,uname)
    return render(request, 'wishlist_display.html', {'pdtdata': mylist,'unm':usernm})




def cartdisplay(request):
    usernm = request.session['uname']
    a=cartmodel.objects.all()
    pname = []
    price = []
    pdtimg = []
    desc = []
    id = []
    username=[]
    for i in a:
        un=i.username
        username.append(un)
        pn = i.pnm
        pname.append(pn)
        prc = i.prc
        price.append(prc)
        img = i.pdtimg
        pdtimg.append(str(img).split('/')[-1])
        ds = i.dsc
        desc.append(ds)
        pid = i.id
        id.append(pid)
        mylist = zip(pname, price, pdtimg, desc, id , username)
    return render(request, 'cart_display.html', {'pdtdata': mylist,'uname':usernm})



def cartpdtremove(request,id):
    a=cartmodel.objects.get(id=id)
    a.delete()
    return redirect(cartdisplay)


def wishlistpdtremove(request, id):
    a=wishlistmodel.objects.get(id=id)
    a.delete()
    return redirect(wishlistdisplay)



def cartpdtbuy(request,id):
    a=cartmodel.objects.get(id=id)
    img=str(a.pdtimg).split('/')[-1]
    if request.method=='POST':
        # image=request.FILES['img']
        name=request.POST.get('pname')
        price=request.POST.get('price')
        desc=request.POST.get('dscptn')
        quantity=request.POST.get('qnty')
        b=buymodel(pnm=name, prc=price, dsc=desc, qty=quantity)
        b.save()
        total=int(price)*int(quantity)    # to get total price of product
        return render(request,'final_bill.html',{'nm':name, 'prc':price, 'qty':quantity, 'total':total, 'img':img})
    return render(request, 'cartpdtbuy.html', {'a':a, 'img':img})




def cardpayment(request):
    if request.method=='POST':
        a=cardpaydetailsform(request.POST)
        if a.is_valid():
            cname=a.cleaned_data['cardname']
            cnum=a.cleaned_data['cardnum']
            exp=a.cleaned_data['cardexpdate']
            securitycode=a.cleaned_data['securitycode']
            print(cname)
            b=cardpaydetailsmodel(cardname=cname, cardnum=cnum, cardexpdate=exp, securitycode=securitycode)
            b.save()
            dt=datetime.date.today()
            futrdt=dt+timedelta(15)   #timedelta(this fn is used to get the future date... (current date+15) )
            return render(request, 'order_status.html', {'date':futrdt})
    return render(request, 'card_payment.html')




def shopnotification(request):
    return render(request,'shop_notification.html')


