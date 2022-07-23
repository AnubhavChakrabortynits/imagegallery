from curses.ascii import HT
import imp
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import SignupForm

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Album,Photo

@login_required(login_url='/login/')
def gallery(request):
    scategory=request.GET.get('category')
    category=None
   
    user=request.user

    sidecategory=Album.objects.filter(user=user)
    if(scategory!=None):
        category=Album.objects.filter(user=user,title=scategory)
    else:
        category=Album.objects.filter(user=user)

    allpics=[]
    for i in category:
    
        allpics.append(Photo.objects.filter(category=i))
         
    photoobj=[]
    for i in allpics:
        for j in i:
            photoobj.append(j)
    
    if(scategory==None):
        scategory="ALL"
    print(photoobj)
    print(category)
    context={"album":sidecategory,"pics":photoobj,'category':scategory}
    return render(request,'gallery.html',context)

@login_required(login_url='/login/')
def viewphoto(request,pk):

    photo=Photo.objects.get(id=pk)
    
    return render(request,'photo.html',{"photo":photo})


@login_required(login_url='/login/')
def addphoto(request):
    if(request.method=='POST'):
        data=request.POST
        category=None
        image=request.FILES.get('image')
        if(data['category']!='none'):
            print(data['category'])
            category=Album.objects.get(title=data['category'],user=request.user)
            print(category,type(category))
            print("album is",request.user)
        elif(data['newcategory']!=''):
            category,created=Album.objects.get_or_create(title=data['newcategory'],user=request.user)
        else:
            category=None

        photo=Photo.objects.create(category=category,description=data['description'],title=data['title'],image=image)
        photo.save()
        
        return HttpResponseRedirect('/')    
         
    
    category=Album.objects.filter(user=request.user)
    return render(request,'add.html',{"category":category})

def loginuser(request):
    if(request.method=='POST'):
        fm=AuthenticationForm(request=request,data=request.POST)
        if(fm.is_valid()):
            uname=fm.cleaned_data['username']
            pword=fm.cleaned_data['password']
            user=authenticate(username=uname,password=pword)
            if(user is not None):
                login(request,user)
                messages.success(request,'Welcome..We wish you have a wondeful experiencewith pixaStore')
                return HttpResponseRedirect('/')
            else:
                messages.error(request,'No Such User...plz Enter Correct Credentials')   
                fm=AuthenticationForm()
                return render(request,'login.html',{'form':fm}) 
 
        else:
            messages.error(request,'Plz enter valid data')
            fm=AuthenticationForm()
            return render(request,'login.html',{'form':fm}) 

    fm=AuthenticationForm()           
    return render(request,'login.html',{'form':fm})

def register(request):
    if(request.method=='POST'):
        fm=SignupForm(request.POST)
        if(fm.is_valid()):
            fm.save()
            messages.success(request,"Account Created Successfully")
            return HttpResponseRedirect('/login/')
        else:
            messages.error(request,'Username or password or email is invalid ..Plz enter corect details')
            return HttpResponseRedirect('/register/')


    fm=SignupForm()
    return render(request,'register.html',{'form':fm})


@login_required(login_url='/login/')
def logoutuser(request):
    logout(request)
    messages.success(request,'Successfully Logged Out..Hope you had a Wonder Experience With PixaStore')
    return HttpResponseRedirect('/login/')