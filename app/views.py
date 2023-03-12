from django.shortcuts import render,redirect
from .models import profile,attendence
from django.contrib import messages
import cv2
from datetime import datetime

from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User

from django.http.response import StreamingHttpResponse
from .camera import VideoCamera,IPWebCam

from cv2 import VideoCapture 
cam = VideoCapture(0)

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import numpy as np
from keras_facenet import FaceNet
embedder = FaceNet()

# Create your views here.
def mark(request):
    result=False
    min_dist = 9999
    identity = ""
    if request.method=="POST":
        result, image = cam.read()
    if result:
        detections = embedder.extract(image, threshold=0.95)
        #print(detections)
        if len(detections)<1 or len(detections)>1:
             messages.info(request,"face not detected")
             return redirect("/")
        encoding=detections[0]['embedding']
        all=profile.objects.values_list("sap","pencoding")
        #print(all)
        for i in all:
            x=np.fromstring(i[1], sep=' ').reshape(512, )
            #print(encoding,x)
            dist=np.linalg.norm(encoding - x)
            print("d=",dist)
            if(dist < min_dist):
                min_dist = dist
                identity = i[0]
        threshold=0.95
        if min_dist < threshold:
            entry=attendence.objects.create(sap=identity,date=datetime.today().strftime('%Y-%m-%d'))
            messages.error(request,"attendence marked for "+str(identity))
            return redirect("/")
        else:
            messages.error(request,"no matching faces")
            return redirect("/")
    #print(identity,min_dist) 
    return render(request,"mark.html")   
'''print('Min dist: ',min_dist)
threshold=0.2
if min_dist < threshold:
	cv2.putText(frame, "Face : " + identity[:-1], (x, y - 50), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
	cv2.putText(frame, "Dist : " + str(min_dist), (x, y - 20), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
else:
	cv2.putText(frame, 'No matching faces', (x, y - 20), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)
'''


def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#Method for laptop camera
def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
                    #video type
					content_type='multipart/x-mixed-replace; boundary=frame')



def register(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        sap=request.POST.get("sap")
        pp=request.FILES.get("pp")
        psw1=request.POST.get("psw1")
        psw2=request.POST.get("psw2")
        #print(sap,pp,psw1,psw2)
        if User.objects.filter(username=sap).exists():
            messages.error(request,"User already exists ")
            return redirect("register")
        elif User.objects.filter(email=email).exists():
            messages.error(request,"Email taken ")
            return redirect("register")
        elif psw1!=psw2:
            messages.error(request,"passwords dont match ")
            return redirect("register")
        else:
            u=User.objects.create_user(username=sap,email=email,password=psw1)
            u.save()
            ap=profile.objects.create(u=u,name=name,sap=sap,email=email,pp=pp)
            ap.save()
            image="media/"+ap.pp.name
            detections = embedder.extract(image, threshold=0.95)
            #print(detections[0]['embedding'])
            pencoding=detections[0]['embedding']
            s=str(pencoding)
            ap.pencoding=s[1:-1]
            ap.save()
            #x=np.fromstring(s[1:-1], sep=' ').reshape(512, )
            messages.error(request,"user registeration complete ")
            return redirect("register")
                
    return render(request,"register.html")

