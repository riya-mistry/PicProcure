from django.shortcuts import render, redirect
from django.http import HttpResponse
import os, uuid
from django.core.files.storage import FileSystemStorage
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from azure.storage.blob import generate_container_sas, ContainerSasPermissions
from datetime import datetime, timedelta
conn_str = "DefaultEndpointsProtocol=https;AccountName=demoblobstorage101;AccountKey=rnT6wujj8Pmh6P1HjtH6p3KfRr6deJcWLwgFgoIpGKYzSk+EOHt+bfIE4ixtIB40yfhc10aLAKKYy91h1xS+4A==;EndpointSuffix=core.windows.net"
Account_name="demoblobstorage101"

# Create your views here.
def home(request):
    return render(request,'uploadFiles/base.html')
def index(request):
    return render(request,'uploadFiles/index.html')
def demoupload(request):
    if request.method == 'POST' and request.FILES.getlist('myfile'):
        myfile12 = request.FILES.getlist('myfile')
        print (myfile12)
        for myfile in myfile12:
            print (myfile)
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            
            actual_file = os.path.join(fs.base_location,filename)
            blob_service_client = BlobServiceClient.from_connection_string(conn_str)
            container_name = "riya"
            try:
                container_client = blob_service_client.create_container(container_name,public_access='blob')
            except Exception :
                pass
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=myfile.name)   
            with open(actual_file, "rb") as data:
                blob_client.upload_blob(data)
            fs.delete(filename)
            uploaded_file_url = fs.url(filename)
        return render(request, 'uploadFiles/demoupload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'uploadFiles/demoupload.html')
def uploaded(request):
    if request.method == "POST":
        blob_name = request.POST.get('image_name','')
        deleteFile(blob_name)    
    return  redirect(viewFiles)
def viewFiles(request):
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    container_name = "riya"
    container_client  = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs()
    urls = []
    for blob in blob_list:
        urls.append(get_img_url_with_blob_sas_token(blob.name))
    context = {'images': urls}
   
    return render (request,'uploadFiles/viewFiles.html',context = context)

def get_img_url_with_blob_sas_token(blob_name):
    """blob_sas_token = generate_blob_sas(
        account_name='demoblobstorage101',
        container_name='folder1',
        blob_name=blob_name,
        account_key="rnT6wujj8Pmh6P1HjtH6p3KfRr6deJcWLwgFgoIpGKYzSk+EOHt+bfIE4ixtIB40yfhc10aLAKKYy91h1xS+4A==",
        permission=ContainerSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)"""
    
    blob_url_with_blob_sas_token = f"https://demoblobstorage101.blob.core.windows.net/riya/"+blob_name
    return blob_url_with_blob_sas_token

def deleteFile(blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    container_name = "folder1"
    container_client  = blob_service_client.get_container_client(container_name)
    container_client.delete_blob(blob_name)
def deleteContainer(container_name):
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    blob_service_client.delete_container(container_name)
def getContainerDeletePage(request):
    if request.method == "POST":
        deleteContainer(request.POST.get('container_name',''))
        return redirect(demoupload)
    else:
        return render(request,'uploadFiles/deleteContainer.html')
