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
# Create your views here.


def combine(request):
    cluster('felicific','output','profile_pics')
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



def cluster(event,event_output,profile_pics):
    md = AzureMediaStorage()
    block_blob_service = BlockBlobService(account_name=md.account_name,account_key=md.account_key)
       
    predictor_path = 'shape_predictor_5_face_landmarks.dat' # Download from http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2
    face_rec_model_path = 'dlib_face_recognition_resnet_model_v1.dat' # Download from http://dlib.net/files/shape_predictor_5_face_landmarks.dat.bz2
    
    faces_folder_path = block_blob_service.list_blobs(container_name=event)
    output_folder = event_output
    check_folder = block_blob_service.list_blobs(container_name=profile_pics)
    
    username_list = []
    for f in check_folder:
        username_list.append(f.name)
    """t = sys.argv[3]
    for root, dirs, files in os.walk(t):
        for file in files:
            #append the file name to the list
         username_list.append(os.path.join(root, file))"""
    #print(username_list)
    detector = dlib.get_frontal_face_detector() #a detector to find the faces
    sp = dlib.shape_predictor(predictor_path) #shape predictor to find face landmarks
    facerec = dlib.face_recognition_model_v1(face_rec_model_path) #face recognition model

    descriptors = []
    images = []
    output_list = []

    """for f in glob.glob(os.path.join(check_folder, "*.jpg")):
        print("Processing file: {}".format(f))
        img1 = dlib.load_rgb_image(f)"""

    for img in check_folder:
        print('Processing file:{}',format(img))
    
        img1 = dlib.load_rgb_image(img)



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
            images.append((img1, shape))

        # Load the images from input folder
        """for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):
        print("Processing file: {}".format(f))
        img = dlib.load_rgb_image(f)"""
        for f in faces_folder_path:
            print("Processing file: {}".format(f))
            img = dlib.load_rgb_image(f)

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
            images.append((img, shape))
    # Cluster the faces.  
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
        img ,shape = images[index]
        #file_path = os.path.join(output_folder_path,"face_"+str(k)+"_"+str(i))
        md.azure_container = 'output'+ str(i)
            
        for k, index in enumerate(indices):
            #dlib.save_face_chip(img, shape, file_path, size=1000, padding = 2)
            md._save(img.name,img)
            if 0 == k:
                output_list.append("ouput/output"+str(i)+"/face_0"+"_"+str(i)+".jpg")