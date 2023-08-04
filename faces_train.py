import os 
from PIL import Image
import numpy as np 
import cv2
import pickle

#walking throught the directory 

base_dir=os.path.dirname(os.path.abspath(__file__))
#setting up the base directory to the curent directory in which this is saves i am doing this because the base directory has both this py file and the folder for the images

image_dir=os.path.join(base_dir,"images")
#creating a path for images folder
#root-> folder for perticular person 
#file-> file name of the image

#creating id's 
current_id=0
label_ids={}
x_train=[] #has the actual pictuer values 
y_labels=[] #has the actual no for the labels 
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

recognizer=cv2.face.LBPHFaceRecognizer_create()


for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith("jpg") or file.endswith("png") or file.endswith("jpeg"):
            path=os.path.join(root,file)
            lable=os.path.basename(os.path.dirname(path)).replace(" ","-").lower()
            #print(lable,path)
            pil_image=Image.open(path).convert("L") #opening up the image at the path and converting it to gray
            #resizing the images
            size=(550,550)
            final_img=pil_image.resize(size,Image.LANCZOS)



            img_array=np.array(final_img,"uint8") #convertint it to a numpy array that is converting the image to numbers

            #creating the id if it is not already there
            if not lable in label_ids:
                label_ids[lable]=current_id
                current_id+=1

            id=label_ids[lable]
            #print(img_array)
            #print(id)
            #doing face detection inside the actual image
            faces=face_cascade.detectMultiScale(img_array,scaleFactor=1.5, minNeighbors=5)

            for(x,y,w,h) in faces:
                roiImg= img_array[y:y+h , x : x+ w]
                x_train.append(roiImg)
                y_labels.append(id)

#print(y_labels)
#print(x_train)
#saving the lables to a pickel file we need these to eventually predict what those really are (here the person)
with open("labels.pickle","wb") as f: 
    pickle.dump(label_ids,f)

#now train the model 
#putting the training data that is the numpy arrays from region of intrust found on the image saved and converting the lables into numpy array as well 
recognizer.train(x_train,np.array(y_labels))
recognizer.save("trainner.yml")