from django.shortcuts import render, redirect
from django.http import HttpResponse
from PicProcure.custom_azure import AzureMediaStorage
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from azure.storage.blob import BlockBlobService 
conn_str = "DefaultEndpointsProtocol=https;AccountName=picprocurestorageaccount;AccountKey=febaaAtjhuePtOvpT5wI8o0OW8r16vu0NLy88/WUASiF02xFqZ7AL6lPeiXin11/oB5BOxvynZSGR6Vj4JGEZw==;EndpointSuffix=core.windows.net"
Account_name="picprocurestorageaccount"

# Create your views here.
@login_required(login_url ='/users/login')
def home(request):
    #viewFiles(request)
    return render(request,'uploadFiles/base.html',{"full_name": request.session['user_name']})

def fileupload(request):
    if request.method == 'POST' and request.FILES.getlist('myfile'):
        myfile12 = request.FILES.getlist('myfile')
        #print (myfile12)
        md = AzureMediaStorage()
        block_blob_service = BlockBlobService(account_name=md.account_name, account_key=md.account_key)
        blob_containter = block_blob_service.create_container('felicific',public_access='Blob') 
        
        md.location = 'event'
        md.azure_container = 'felicific'
        for myfile in myfile12:
            print (myfile)
            md._save(myfile.name,myfile)
            #md.save(myfile.name,myfile)
        return render(request, 'uploadFiles/demoupload.html', {
            'uploaded_file_url': 'uploaded successfully'
        })
    return render(request, 'uploadFiles/demoupload.html')

def viewFiles(request):
    md = AzureMediaStorage()
    md.location='felicific'
    #md._blob_service(connection_string=conn_str).list_blob_names(container_name='')
    #files = md.connection_string(conn_str).get_container_client(container_name="media").list_blob_names()
    #files = md._blob_service(connection_string=conn_str).list_blob_names(container_name='media',prefix="Event")
    #md._blob_service(connection_string=conn_str).list_containers()
    block_blob_service = BlockBlobService(account_name=md.account_name, account_key=md.account_key)
    files = block_blob_service.list_blobs('felicific')
    urls = []
    for f in files:
        urls.append(f.name)
        
    context = {'images': urls}
   
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
