from django.shortcuts import render, redirect
from django.http import HttpResponse
from PicProcure.custom_azure import AzureMediaStorage
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from azure.storage.blob import BlockBlobService 
from users.models import Events


# Create your views here.
@login_required(login_url ='/users/login')
def home(request):
    return render(request,'uploadFiles/base.html',{"full_name": request.session['user_name']})

@login_required(login_url ='/users/login')
def fileupload(request,eventname):
    if request.method == 'POST' and request.FILES.getlist('myfile'):
        myfile12 = request.FILES.getlist('myfile')
        #print (myfile12)
        md = AzureMediaStorage()
        block_blob_service = BlockBlobService(account_name=md.account_name, account_key=md.account_key)
        md.azure_container = eventname
        for myfile in myfile12:
            print (myfile)
            md._save(myfile.name,myfile)
        return render(request, 'uploadFiles/demoupload.html', {'uploaded_file_url': 'uploaded successfully'})
    event = Events.objects.get(event_name = eventname)
    test = datetime.now().minute < event.creation_time.minute + 1
    return render(request, 'uploadFiles/demoupload.html',{"test":test})

@login_required(login_url ='/users/login')
def viewFiles(request,eventname):
    md = AzureMediaStorage()
    md.azure_container=eventname
    block_blob_service = BlockBlobService(account_name=md.account_name, account_key=md.account_key)
    files = block_blob_service.list_blobs(eventname)
    urls = []
    for f in files:
        urls.append(f.name)
    context = {'images': urls,'event':eventname}
   
    return render (request,'uploadFiles/viewFiles.html',context=context)
        



def deleteFile(blob_name):
    md = AzureMediaStorage()
    md.location = 'samyak'
    md.delete(blob_name)
    """blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    container_name = "folder1"
    container_client  = blob_service_client.get_container_client(container_name)
    container_client.delete_blob(blob_name)"""
def deleteContainer(container_name):
    """blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    blob_service_client.delete_container(container_name)"""
def getContainerDeletePage(request):
    if request.method == "POST":
        deleteContainer(request.POST.get('container_name',''))
        return redirect(fileupload)
    else:
        return render(request,'uploadFiles/deleteContainer.html')
