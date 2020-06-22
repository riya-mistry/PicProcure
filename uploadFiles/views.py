from django.shortcuts import render, redirect
from django.http import HttpResponse
import os, uuid
from django.core.files.storage import FileSystemStorage
from PicProcure.custom_azure import AzureMediaStorage
#from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
#from azure.storage.blob import generate_blob_sas, BlobSasPermissions
#from azure.storage.blob import generate_container_sas, ContainerSasPermissions
from datetime import datetime, timedelta
conn_str = "DefaultEndpointsProtocol=https;AccountName=demoblobstorage101;AccountKey=rnT6wujj8Pmh6P1HjtH6p3KfRr6deJcWLwgFgoIpGKYzSk+EOHt+bfIE4ixtIB40yfhc10aLAKKYy91h1xS+4A==;EndpointSuffix=core.windows.net"
Account_name="demoblobstorage101"

# Create your views here.
def home(request):
    viewFiles(request)
    return render(request,'uploadFiles/base.html')
    
def fileupload(request):
    if request.method == 'POST' and request.FILES.getlist('myfile'):
        myfile12 = request.FILES.getlist('myfile')
        print (myfile12)
        for myfile in myfile12:
            print (myfile)
            md = AzureMediaStorage()
            md.location = 'samyak'
            fu = md.save(myfile.name,myfile)
            uploaded_file_url = md.url(fu)
        return render(request, 'uploadFiles/demoupload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'uploadFiles/demoupload.html')

def viewFiles(request):
    md = AzureMediaStorage()
    md.location='samyak'
    files = md._blob_service(connection_string=conn_str).list_blob_names(container_name='media')
    urls = []
    for f in files:
        urls.append(f)
        
    context = {'images': urls}
   
    return render (request,'uploadFiles/viewFiles.html',context=context)



def deleteFile(blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    container_name = "folder1"
    container_client  = blob_service_client.get_container_client(container_name)
    container_client.delete_blob(blob_name)
def deleteContainer(container_name):
    """blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    blob_service_client.delete_container(container_name)"""
def getContainerDeletePage(request):
    if request.method == "POST":
        deleteContainer(request.POST.get('container_name',''))
        return redirect(demoupload)
    else:
        return render(request,'uploadFiles/deleteContainer.html')
