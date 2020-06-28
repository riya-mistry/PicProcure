from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from users.models import Events,Users
# Create your views here.

@login_required(login_url='/users/login')
def new_event(request):
    if request.method == "POST":
        user = Users.objects.get(user_name=request.session['user_name'])
        #u = user.objects.get(user_name= request.session['user_name'])
        event = Events()
        event.event_name = request.POST.get('event_name','')
        event.description = request.POST.get('description','')
        event.creation_date = datetime.now()
        event.event_owner = user.user_id
        event.save()
        return HttpResponse(event)
        

    return render(request,'events/new-event.html')