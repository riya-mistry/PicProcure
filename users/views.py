from django.shortcuts import render,HttpResponse
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
    return render(request,'users/signup.html')
