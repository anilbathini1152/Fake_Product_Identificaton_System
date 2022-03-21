from .models import Manudetails,Products
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout 
from shared.models import Isdist
from dist.models import ProfImg


# Create your views here.
def manuhome(request):
    if request.user.is_authenticated:
        sts=Isdist.objects.get(username=request.user.username)
        if sts.status==2:
            return render(request,"manuhome.html")
        else:
            return redirect('home')
    else:
        return redirect('home')

def mprof(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            contact=request.POST["cntctno"]
            orgdata=Manudetails.objects.filter(id=request.user.username)
            if orgdata.count()==0:
                orgudata=Manudetails.objects.create(id=request.user.username,contact=contact)
                messages.success(request,"Profile Updated Successfully")
                return redirect('mprof')
            else:
                orgudata=Manudetails.objects.get(id=request.user.username)
                if len(contact)!=0:
                    orgudata.contact=contact
                orgudata.save()
                messages.success(request,"Profile Updated Successfully")
                return redirect('mprof')      
        else:
            orgdata=Manudetails.objects.filter(id=request.user.username)
            return render(request,"manuprofile.html",{'org':orgdata})
    else:
        return redirect('home')

def profimgup(request):
    if request.user.is_authenticated:
        sts=Isdist.objects.get(username=request.user.username)
        if sts.status==2:
            pic=request.FILES['profimg']
            img=ProfImg(prof_img=pic)
            img.save()
            orgudata=Manudetails.objects.get(id=request.user.username)
            if len(pic)!=0:
                orgudata.prof="/profiles/"+str(pic)
            orgudata.save()
            messages.success(request,"Profile image Updated Successfully")
            return redirect('mprof')  
        else:
            return redirect('home')
    else:
        return redirect('home')

def genQr(request,prod):
    import qrcode
    import cv2
    img=qrcode.make(prod.pid)
    s=str(prod.pid)
    s=s[len(s)//2:len(s)-1]
    img.save("C:/Users/anilb/Desktop/QRS/prdct"+s+".jpg")
                # print(prod.pid)
    messages.success(request,"Product added successfully")
    return render(request,"manuhome.html")

def addprod(request):
    if request.user.is_authenticated:
        sts=Isdist.objects.get(username=request.user.username)
        if sts.status==2:
            if request.method=='POST':
                name=request.POST["pname"] 
                mndate=request.POST["mdate"] 
                exdate=request.POST["edate"] 
                prod=Products.objects.create(pname=name,mdate=mndate,edate=exdate,manufusrname=request.user.username)
                prod.save()
                return genQr(request,prod)

        else:
            return redirect('home')
    else:
        return redirect('home')

