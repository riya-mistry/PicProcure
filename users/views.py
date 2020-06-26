from django.shortcuts import render,HttpResponse
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf 
from .models import Users
from PicProcure.custom_azure import AzureMediaStorage
# Create your views here.
def register(request):
    if request.method == "POST":
        user = Users()
        user.user_name = request.POST.get('user_name','')
        user.first_name = request.POST.get('first_name','')
        user.last_name = request.POST.get('last_name','')
        user.email_id = request.POST.get('email_id','')
        user.password = request.POST.get('password','')
        repassword = request.POST.get('re-password','')
        if user.password == repassword:
            file = request.FILES.get('profile_pic')
            user.profile_pic = user.user_name
            md = AzureMediaStorage()
            md.location= "Profile_Pics"
            pp = md.save(user.first_name + user.last_name,file)
        user.save()
        render(request,'users/login.html')
    return render(request,'users/signup.html')

def login(request):
    c = {}
    c.update(csrf(request))
    return render(request,'users/login.html', c)

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    try:
        user= Users.objects.get(user_name=username,password=password)
        #user= Users.objects.raw('Select * from users_users where user_name=%s and password=%s',[username],[password])
        #user = auth.authenticate(user_name=username, password=password)
        if user is not None:
            #auth.login(request, user)
            return render(request,'uploadFiles/base.html', {"full_name": user.first_name})

        else:
            return render(request,'users/login.html', {"Invalid_msg": "Invalid Username or Password"})
    except:
        return render(request,'users/login.html', {"Invalid_msg": "Invalid Username or Password"})

def logout(request):
    #auth.logout(request)
    return render(request,'users/login.html')