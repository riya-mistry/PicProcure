from django.shortcuts import render
from django.http import HttpResponse
import os, uuid
from django.core.files.storage import FileSystemStorage
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
conn_str = "DefaultEndpointsProtocol=https;AccountName=demoblobstorage101;AccountKey=rnT6wujj8Pmh6P1HjtH6p3KfRr6deJcWLwgFgoIpGKYzSk+EOHt+bfIE4ixtIB40yfhc10aLAKKYy91h1xS+4A==;EndpointSuffix=core.windows.net"

# Create your views here.
def index(request):
    return render(request,'uploadFiles/index.html')
def demoupload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        folder_name = request.POST.get('folder_name','')
        print(folder_name)
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        
        actual_file = os.path.join(fs.base_location,filename)
        blob_service_client = BlobServiceClient.from_connection_string(conn_str)
        container_name = 'riya'
        if blob_service_client.get_container_client(container_name) is None:
            container_client = blob_service_client.create_container(container_name)
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
        s = request.FILES['file123']
        print(s)        
    return HttpResponse("helo world" +str(s))
    