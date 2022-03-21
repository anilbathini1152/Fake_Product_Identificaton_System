from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout 
from .models import Isdist,Userdetails
from dist.models import ProfImg,QRUp
from uuid import UUID
from manuf.models import Products

# Create your views here.
def home(request):
    return render(request,"home.html")

# Register
def usignup(request):

    if request.method =='POST':
        try:
            #parameters gathering
            username=request.POST["username"]
            fname=request.POST["fname"]
            lname=request.POST["lname"]
            email=request.POST["email"]
            password=request.POST["password"]
            cpassword=request.POST["cpassword"]

            # validation of data
            # checking if username contains any other characters
            if username.isalnum():
                # checking if usrname len greater than 6
                if len(username)>=6:
                    # checking if password and conform password matched and password length
                    if len(password)>=8:
                        if password==cpassword:
                            myuser=User.objects.create_user(username=username,password=password,email=email)
                            myuser.first_name=fname
                            myuser.last_name=lname
                            myuser.save()
                            # saving in a seperate file to ensure if he is a Manufacturer, Distribuntor 
                            isdist=Isdist.objects.create(id=myuser.id,status=0,username=myuser.username)
                            isdist.save()
                            messages.success(request,"Registration success")
                            return redirect('home')
                        else:
                            messages.error(request,"Password and confirm password don't match")
                            return redirect('home')
                    else:
                        messages.error(request,"Password should be atleast 8 characters")
                        return redirect('home')
                else:
                    messages.error(request,"User name should be greater than 6 letters")
                    return redirect('home') 
            else:
                messages.error(request,"User name should contain only alphabets and numbers")
                return redirect('home')   
        except IntegrityError as e: 
                messages.error(request,"User name taken, try another")
                return redirect('home') 
    else:
        return HttpResponse("404 Page Not Found")


# Login
def ulogin(request):
    if request.method =='POST':
            #parameters gathering
            username=request.POST["username"]
            password=request.POST["password"]
            status=request.POST["category"]

            #organiser and user streams for login
            if status=='0':
                try:
                    validators=Isdist.objects.get(username=username)
                except Isdist.DoesNotExist:
                    messages.error(request,"Validation failed")
                    return redirect('home')
                if validators.status==0:
                    user=authenticate(username=username,password=password)
                    if user is not None:
                        login(request,user)
                        messages.success(request,"Successfully Logged in as "+str(user.username))
                        return redirect('home')
                    else:
                        messages.error(request,"invalid Credentials")
                        return redirect('home')
                else:
                    messages.error(request,"No user account with given credentials")
                    return redirect('home')
            elif  status=='1':
                try:
                    validators=Isdist.objects.get(username=username)
                except Isdist.DoesNotExist:
                    messages.error(request,"Validation failed")
                    return redirect('home')
                validators=Isdist.objects.get(username=username)
                if validators.status==1:
                    user=authenticate(username=username,password=password)
                    if user is not None:
                        login(request,user)
                        messages.success(request,"Successfully Logged in as "+str(user.username))
                        return redirect('disthome')
                    else:
                        messages.error(request,"invalid Credentials")
                        return redirect('home')
                else:
                    messages.error(request,"No distributer account with given credentials")
                    return redirect('home')
            else:
                try:
                    validators=Isdist.objects.get(username=username)
                except Isdist.DoesNotExist:
                    messages.error(request,"Validation failed")
                    return redirect('home')
                validators=Isdist.objects.get(username=username)
                if validators.status==2:
                    user=authenticate(username=username,password=password)
                    if user is not None:
                        login(request,user)
                        messages.success(request,"Successfully Logged in as "+str(user.username))
                        return redirect('manuhome')
                    else:
                        messages.error(request,"invalid Credentials")
                        return redirect('home')
                else:
                    messages.error(request,"No Manufacturer account with given credentials")
                    return redirect('home')
    else:
        return HttpResponse("404 Page not found")


#Logout
def ulogout(request):
        logout(request)
        messages.success(request,"Successfully Logged out")
        return redirect('home')



#Userfprofile
def uprof(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            contact=request.POST["cntctno"]
            dob=request.POST["dob"]
            gender=request.POST["gendr"]
            orgdata=Userdetails.objects.filter(id=request.user.username)
            if orgdata.count()==0:
                orgudata=Userdetails.objects.create(id=request.user.username,contact=contact,dob=dob,gender=gender)
                messages.success(request,"Profile Updated Successfully")
                return redirect('uprof')
            else:
                vald=Userdetails.objects.get(id=request.user.username)
                if len(contact)!=0:
                    vald.contact=contact
                if len(dob)!=0:
                    vald.dob=dob
                if len(gender)!=0:
                    vald.gender=gender
                vald.save()
                messages.success(request,"Profile Updated Successfully")
                return redirect('uprof')      
        else:
            orgdata=Userdetails.objects.filter(id=request.user.username)
            return render(request,"userprofile.html",{'org':orgdata})
    else:
        return redirect('home')

def qr_image_view(request):
    if request.user.is_authenticated:
        sts=Isdist.objects.get(username=request.user.username)
        if sts.status==0:
         
            pic=request.FILES['QRupload']
            img=QRUp(qr_img=pic)
            img.save()
            return qrImgVerify(pic,request)
        else:
            return redirect('home')
    else:
        return redirect('home')

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
    return render(request,"scanp.html",{'val':prod})


def profimgup(request):
    if request.user.is_authenticated:
        sts=Isdist.objects.get(username=request.user.username)
        if sts.status==0:
            pic=request.FILES['profimg']
            img=ProfImg(prof_img=pic)
            img.save()
            orgudata=Userdetails.objects.get(id=request.user.username)
            if len(pic)!=0:
                orgudata.proflepic="/profiles/"+str(pic)
            orgudata.save()
            messages.success(request,"Profile image Updated Successfully")
            return redirect('uprof')  
        else:
            return redirect('home')
    else:
        return redirect('home')       