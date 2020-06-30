from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from users.models import Events,Users
from azure.storage.blob import BlockBlobService 
from PicProcure.custom_azure import AzureMediaStorage
import sys
import time
import os
import dlib
import glob
import cv2
from PIL import Image
import subprocess as sbp
from PIL import ImageChops,Image
import math, operator
import argparse
import imutils
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import face_recognition
import re
import shutil
import io
from PIL import Image
import urllib.request
import numpy
def combine(request):
    cluster('felicific','output','profile-pics')
    return HttpResponse("hello")        



@login_required(login_url='/users/login')
def new_event(request):
    if request.method == "POST":
        user = Users.objects.get(user_name=request.session['user_name'])
        #u = user.objects.get(user_name= request.session['user_name'])
        event = Events()
        event.event_name = request.POST.get('event_name','')
        event.description = request.POST.get('description','')
        event.creation_date = datetime.now()
        event.event_owner = user
        event.save()
        return HttpResponse(event)
        

    return render(request,'events/new-event.html')




def cluster(request):
    start = time.time()
    md = AzureMediaStorage()
    block_blob_service = BlockBlobService(account_name=md.account_name,account_key=md.account_key)
    # Download the pre trained models, unzip them and save them in the save folder as this file
    
    predictor_path = 'C:/Users/User/Desktop/PicProcure/PicProcure/events/shape_predictor_5_face_landmarks.dat'
    face_rec_model_path = 'C:/Users/User/Desktop/PicProcure/PicProcure/events/dlib_face_recognition_resnet_model_v1.dat'

    faces_folder_path = block_blob_service.list_blobs(container_name='felicific')
    output_folder = 'output'
    check_folder = block_blob_service.list_blobs(container_name='profile-pics')

    username_list = []
    for f in check_folder:
        username_list.append(f.name)
    print(username_list)

    detector = dlib.get_frontal_face_detector() #a detector to find the faces
    sp = dlib.shape_predictor(predictor_path) #shape predictor to find face landmarks
    facerec = dlib.face_recognition_model_v1(face_rec_model_path) #face recognition model

    descriptors = []
    images = []
    output_list = []
    
    """for img in check_folder:
        
        print('Processing file:{}',format(img.name))
        url = "https://picprocurestorageaccount.blob.core.windows.net/profile-pics/"+ img.name
        #img1 = dlib.load_rgb_image(urllib.request.urlopen(url).read())
        #win = dlib.image_window()
        img1 = numpy.array(Image.open(io.BytesIO(urllib.request.urlopen(url).read())))
        #win.set_image(img1)
        
    # Ask the detector to find the bounding boxes of each face. The 1 in the second argument indicates that we should upoutput_listple the image 1 time. This will make everything bigger and allow us to detect more faces.
        dets = detector(img1, 1)
        print("Number of faces detected: {}".format(len(dets)))

    # Now process each face we found.
        for k, d in enumerate(dets):
        # Get the landmarks/parts for the face in box d.
            shape = sp(img1, d)

        # Compute the 128D vector that describes the face in img identified by shape.  
            face_descriptor = facerec.compute_face_descriptor(img1, shape)
            descriptors.append(face_descriptor)
            images.append((img.name,img1, shape)) """     
    print('profile pics ended')    
    for f in faces_folder_path:
        print("Processing file: {}".format(f.name))
        url = "https://picprocurestorageaccount.blob.core.windows.net/felicific/"+ f.name
        #img = dlib.load_rgb_image(f)
        #win = dlib.image_window()
        img = numpy.array(Image.open(io.BytesIO(urllib.request.urlopen(url).read())))
        #win.set_image(img)
        # Ask the detector to find the bounding boxes of each face. The 1 in the second argument indicates that we should upoutput_listple the image 1 time. This will make everything bigger and allow us to detect more faces.
        dets = detector(img, 1)
        print("Number of faces detected: {}".format(len(dets)))
        # Now process each face we found.

        for k, d in enumerate(dets):
        # Get the landmarks/parts for the face in box d.
            shape = sp(img, d)
        # Compute the 128D vector that describes the face in img identified by shape.  
            face_descriptor = facerec.compute_face_descriptor(img, shape)
            descriptors.append(face_descriptor)
            images.append((f.name,img, shape))

        # Cluster the faces.  
    print("event load completed")
    labels = dlib.chinese_whispers_clustering(descriptors, 0.5)
    num_classes = len(set(labels)) # Total number of clusters
    print("Number of clusters: {}".format(num_classes))

    for i in range(0, num_classes):
        indices = []
        class_length = len([label for label in labels if label == i])
        for j, label in enumerate(labels):
            if label == i:
                indices.append(j)
        print("Indices of images in the cluster {0} : {1}".format(str(i),str(indices)))
        print("Size of cluster {0} : {1}".format(str(i),str(class_length)))
        #output_folder_path = output_folder + '/output' + str(i) # Output folder for each cluster
        #os.path.normpath(output_folder_path)
        #os.makedirs(output_folder_path)
        block_blob_service.create_container('output'+ str(i))

    # Save each face to the respective cluster folder
        print("Saving faces to output folder...")
        #img, shape = images[index]
            #file_path = os.path.join(output_folder_path,"face_"+str(k)+"_"+str(i))
        md.azure_container = 'output'+ str(i)
            
        for k, index in enumerate(indices):
            name,img, shape = images[index]
            #dlib.save_face_chip(img, shape, file_path, size=1000, padding = 2)
            #url = "https://picprocurestorageaccount.blob.core.windows.net/felicific/"+ name
            block_blob_service.copy_blob(container_name=md.azure_container,blob_name=name,copy_source="https://picprocurestorageaccount.blob.core.windows.net/felicific/"+ name)
           # md._save(name,img)
            if 0 == k:
                output_list.append("ouput/output"+str(i)+"/face_0"+"_"+str(i)+".jpg")
    return HttpResponse("Succuessfull")