from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout 
from shared.models import Isdist
from .forms import *
from .models import QRUp,Distdetails,ProfImg
from manuf.models import Products
from uuid import UUID

# Create your views here.


#home page for distibuters
def disthome(request):
    if request.user.is_authenticated:
        sts=Isdist.objects.get(username=request.user.username)
        if sts.status==1:
            return render(request,"disthome.html")
        else:
            return redirect('home')
    else:
        return redirect('home')

#Chk the uploaded QR
def qrImgVerify(pic,request):
    import cv2
    d=cv2.QRCodeDetector()
    retval,points,stqr=d.detectAndDecode(cv2.imread("C:/Users/anilb/Desktop/smmrproj/fpis/media/images/"+str(pic)))
    print(retval)
    try:
        uuid_obj=UUID(str(retval))
        try:
            prod=Products.objects.get(pid=retval)
        except (Products.DoesNotExist):
            return render(request,"wrngQR.html")
    except (ValueError):
        return render(request,"wrngQR.html")
    prod.ver=(prod.verfied==0)
    return render(request,"scan.html",{'val':prod})
    
        

# upload the QR image
def qr_image_view(request):
    if request.user.is_authenticated:
        sts=Isdist.objects.get(username=request.user.username)
        if sts.status==1:
            pic=request.FILES['QRupload']
            img=QRUp(qr_img=pic)
            img.save()
            return qrImgVerify(pic,request)
        else:
            return redirect('home')
    else:
        return redirect('home')

def dprof(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            contact=request.POST["cntctno"]
            orgdata=Distdetails.objects.filter(id=request.user.username)
            if orgdata.count()==0:
                orgudata=Distdetails.objects.create(id=request.user.username,contact=contact)
                messages.success(request,"Profile Updated Successfully")
                return redirect('dprof')
            else:
                orgudata=Distdetails.objects.get(id=request.user.username)
                if len(contact)!=0:
                    orgudata.contact=contact
                orgudata.save()
                messages.success(request,"Profile Updated Successfully")
                return redirect('dprof')      
        else:
            orgdata=Distdetails.objects.filter(id=request.user.username)
            return render(request,"distprofile.html",{'org':orgdata})
    else:
        return redirect('home')

def profimgup(request):
    if request.user.is_authenticated:
        sts=Isdist.objects.get(username=request.user.username)
        if sts.status==1:
            pic=request.FILES['profimg']
            img=ProfImg(prof_img=pic)
            img.save()
            try:
                orgudata=Distdetails.objects.get(id=request.user.username)
                if len(pic)!=0:
                    orgudata.prof="/profiles/"+str(pic)
                orgudata.save()
                messages.success(request,"Profile image Updated Successfully")
                return redirect('dprof')  
            except Distdetails.DoesNotExist:
                messages.success(request,"Error uploading image")
                return redirect('dprof')
        else:
            return redirect('home')
    else:
        return redirect('home')


    

def verify_prod(request):
    if request.user.is_authenticated:
        sts=Isdist.objects.get(username=request.user.username)
        if sts.status==1:
            if request.method=="POST":
                chkval=request.POST.get('category',0)
                # print(chkval)
                ids=request.POST.get('pid')
                # print(ids)
                up=Products.objects.get(pid=ids)
                # print(up.pname)
                up.verfied=int(chkval)
                up.distusrname=request.user.username
                up.save()
                messages.success(request,"Response recorded")
                return render(request,"disthome.html")
        else:
            return redirect('home')
    else:
        return redirect('home')