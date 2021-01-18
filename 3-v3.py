# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 11:50:29 2021

@author: DotNet
"""
import tkinter 
from tkinter import *
from PIL import Image, ImageTk
from tkinter.ttk import Button
import os
import time
import cv2
from win32api import GetSystemMetrics

#getting list of pictures in directory
def get_image_paths(input_dir='.'):
    paths = []
    for root, dirs, files in os.walk(input_dir, topdown=True):
        for file in sorted(files):
            if file.endswith(('jpg', 'png')):
                path = os.path.abspath(os.path.join(root, file))
                paths.append(path)
    return paths

def get_img_fit_size(path, scr_w, scr_h):
    image = cv2.imread(path)
    
    # Getting 
    img_w = image.shape[1]
    img_h = image.shape[0]
    
    # when the width of the photo is more than it's height and more than screen width
    if img_w > img_h and img_w > scr_w and img_h > scr_h:
        print("Case 1",img_w, img_h, scr_w, scr_h)
        #determining the image size accouring to the equasion
        # x * img_w = scr_w, then multiply x by the img_h, 
        # so in conclusion we multiply the hight by the same number that we have multiplied the x with
        var = int(img_h*(scr_w/img_w))
        img = ImageTk.PhotoImage(Image.open(path).resize((int(scr_w), var)), Image.ANTIALIAS)
        #print("Scr_w / img_w:", scr_w / img_w, "scr_w:",scr_w, "(scr_w/img_w)*img_h:",img_h*(scr_w/img_w), "scr_w:",scr_w)
        #print("final image width:" ,scr_w, "final image height:",var)
    
    # when the hieght of the image is more than it's width and also more than screen height
    elif img_h > img_w and img_h > scr_h:
        print("Case 2")
        var = int(img_w*(scr_h/img_h))
        img = ImageTk.PhotoImage(Image.open(path).resize((var, int(scr_h)), Image.ANTIALIAS))
    elif img_w <= scr_w or img_h <= scr_h:
        img = ImageTk.PhotoImage(Image.open(path))
        
    elif img_w == img_h and img_w > scr_w:
        print("Case 5")
        img = ImageTk.PhotoImage(Image.open(path).resize(scr_w, scr_h), Image.ANTIALIAS)
    else:
        print("Non of above conditions",img_w, img_h, scr_w, scr_h)
        img = ImageTk.PhotoImage(Image.open(path))
    return img



#getting the screen width and hieight
scr_w = GetSystemMetrics(0)
scr_h = GetSystemMetrics(1)

#Creating tk window
window = Tk(screenName="name")
#making the tk window size equal to the screen size
window.geometry(str(scr_w)+"x"+str(scr_h)+"+0+0")


    #function to make full screen
def fullScreen(event):
    val = window.overrideredirect()
    if(str(val) == 'None'):
        window.overrideredirect(True)
        #print("Make it big")
    elif(str(val) == 'True'):
        window.overrideredirect(False)
        #print("Make it small")
    else:
        print("dam"+str(val))
       
       
# Create Button and add some text
button = Button(window, text = 'Full Screen', command = fullScreen)
#button.pack(side = "bottom", pady = 2)


numOfImages=0 
   
def submit2():
    
    #Get paths
    paths = get_image_paths()
    #read the image 
    #call the function to get the picture object with new size
    global numOfImages
    
    path = paths[numOfImages]
    
    while(numOfImages<=len(paths)-1):#
        
        path = paths[numOfImages]
        numOfImages=numOfImages+1
        
        if(numOfImages>len(paths)):
            numOfImages=0 
        
        #createing canvas and make it equal to the screen width and hight
        canvas = Canvas(window,width=scr_w, height=scr_h, bg='black')
        #gird plays the canvas without it the canvas will not work
        canvas.grid(row=0,column=0)
        
        
        
        img = get_img_fit_size(path, scr_w, scr_h)
        my_image = canvas.create_image(int(scr_w/2),int(scr_h/2),anchor=CENTER, image=img)
        
        path_arr = path.split('\\') # split the direcoties of the image path 
        f_img = (path_arr[-1]) # get the last index of the array of the path
        result = f_img[:-4] # Remve last characters from the image name
        description = result
    
        my_regtangle = canvas.create_rectangle(scr_w/2-250,scr_h/1.15-20,scr_w/2+250,scr_h/1.15+20,fill="black")
        
        my_message = canvas.create_text(scr_w/2,scr_h/1.15,fill="#fff",font="family",text=description,anchor="center")
        window.update()
        time.sleep(2)
    
    window.mainloop()
    
    



button_submit2=Button(window,text="Submit-2",width=10,command=submit2)
button_submit2.grid(row=0,column=3)

   
window.bind('<Double 1>', fullScreen)

window.mainloop()


