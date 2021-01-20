# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 11:50:29 2021

@author: Mohammed S. Hazim
"""
import tkinter
from tkinter import *
from PIL import Image, ImageTk
from tkinter.ttk import *
import os
import time
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

def get_img_fit_size(path, scr_w, scr_h, rotate):
    
    print("Path:", path)
    
    imgsize = ImageTk.PhotoImage(Image.open(path))

    # Getting 
    img_w = imgsize.width()
    img_h = imgsize.height()
    # when the width of the photo is more than it's height and more than screen width
    if img_w > img_h and img_w > scr_w and img_h > scr_h:
        #determining the image size accouring to the equasion
        # x * img_w = scr_w, then multiply x by the img_h, 
        # so in conclusion we multiply the hight by the same number that we have multiplied the x with
        print("Case 1",img_w, img_h, scr_w, scr_h)
        var = int(img_h*(scr_w/img_w))
        img1 = Image.open(path)
        
        
        #checking rotation if requested or not
        if rotate == False:
            img2 = img1.resize(((int(scr_w), var)), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img2)
        elif rotate == True:
            #using transpose function instead of rotate to avoid cropping sides
            img2 = img1.transpose(Image.ROTATE_270)
            #Exchanging hieght with width value positions to make it work correctly
            img3 = img2.resize((var,int(scr_h)), Image.ANTIALIAS)
            #Save the result to img
            img = ImageTk.PhotoImage(img3)
        else:
            print("Missing rotate attribute")

    
    # when the hieght of the image is more than it's width and also more than screen height
    elif img_h > img_w and img_h > scr_h:
        print("Case 2")
        var = int(img_w*(scr_h/img_h))
        img1 = Image.open(path)
        
        
        #checking rotation if requested or not, if rotation is enabled then roate picture befor resizing
        if rotate == False:
            img2 = img1.resize((var, int(scr_h)), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img2)
        elif rotate == True:
            #using transpose function instead of rotate to avoid cropping sides
            img2 = img1.transpose(Image.ROTATE_270)
            #Exchanging hieght with width value positions to make it work correctly
            img3 = img2.resize((int(scr_h),var ), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img3)
        else:
            print("Missing rotate attribute")
        
    elif img_w <= scr_w and img_h <= scr_h:
        print("Case 3")
        img1 = Image.open(path)
        img2 = img1.resize((img_w-out, img_h-out), Image.ANTIALIAS)
        
        #checking rotation if requested or not
        if rotate == False:
            img = ImageTk.PhotoImage(img2)
        elif rotate == True:
            img = ImageTk.PhotoImage(img2.rotate(angle))
        else:
            print("Missing rotate attribute")
        
    elif img_w == img_h and img_w > scr_w:
        print("Case 4")
        img1 = Image.open(path)
        img2 = img1.resize((scr_w, scr_h), Image.ANTIALIAS)
        
        #checking rotation if requested or not
        if rotate == False:
            img = ImageTk.PhotoImage(img2)
        elif rotate == True:
            img = ImageTk.PhotoImage(img2.rotate(angle))
        else:
            print("Missing rotate attribute")
    else:
        print("Non of above conditions",img_w, img_h, scr_w, scr_h)
        img1 = Image.open(path)
        img2 = img1.resize((img_w-out, img_h-out), Image.ANTIALIAS)
        
        #checking rotation if requested or not
        if rotate == False:
            img = ImageTk.PhotoImage(img2)
        elif rotate == True:
            img = ImageTk.PhotoImage(img2.rotate(angle))
        else:
            print("Missing rotate attribute")
            
    return img

#function inputs percentage and number and outputs how much is that percentage in the number
def cal_per_num(percentage, number):
    quotient = percentage / 100
    percentage = quotient * number
    return percentage

#getting the screen width and hieight
scr_w = GetSystemMetrics(0)
scr_h = GetSystemMetrics(1)

#Creating tk window
window = Tk(className="Ragazinana")
#making the tk window size equal to the screen size
window.geometry(str(scr_w)+"x"+str(scr_h)+"+0+0")
#changing window background color to black
window.configure(bg="black")

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

#Our global variable, increase it in the global scope, not only inside the functions
numOfImages=0 
   
def Single_view():
    global timeSleep
    timeSleep = int(timeSleep.get())
    
    #directory = filedialog.askdirectory()
    directory = r"C:\Users\DotNet\Desktop\Ragazinana Data reduced\diashow\4 Random\Portrait"
    #Get paths
    paths = get_image_paths(directory)
    #read the image 
    #call the function to get the picture object with new size
    global numOfImages
    
    path = paths[numOfImages]
    
    while(numOfImages<=len(paths)-1):#if total is 5 pictures then 1st loop 0 <= 6-1 ==> 0 <= 5 ,2nd loop 1 <= 5
        
        path = paths[numOfImages]
        numOfImages=numOfImages+1
        
        if(numOfImages>len(paths)):# if total is 5 pic, 1st loop 0 > 6 /reset the loop
            numOfImages=0 
        
        
        #createing canvas and make it equal to the screen width and hight
        canvas = Canvas(window,width=scr_w, height=scr_h, bg='black')
        #gird plays the canvas without it the canvas will not work
        canvas.grid(row=0,column=0)
        
        
        
        img = get_img_fit_size(path, scr_w, scr_h, False)
        my_image = canvas.create_image(int(scr_w/2),int(scr_h/2),anchor=CENTER, image=img)
        
        
        #Text View
        path_arr = path.split('\\') # split the direcoties of the image path 
        f_img = (path_arr[-1]) # get the last index of the array of the path
        result = f_img[:-4] # Remve last characters from the image name
        description = result
    
        my_regtangle = canvas.create_rectangle(scr_w/2-250,scr_h/1.15-20,scr_w/2+250,scr_h/1.15+20,fill="black")
        
        my_message = canvas.create_text(scr_w/2,scr_h/1.15,fill="#fff",font="family",text=description,anchor="center")
        window.update()
        time.sleep(timeSleep)
    
    window.mainloop()
    
def Multi_view():
    
    global timeSleep
    timeSleep = int(timeSleep.get())
    
    #Getting Directory from user input
    #directory = filedialog.askdirectory()
    directory = r"C:\Users\DotNet\Desktop\Ragazinana Data reduced\diashow\4 Random\Portrait"
    #Get paths
    paths = get_image_paths(directory)
    #read the image 
    #call the function to get the picture object with new size
    global numOfImages
    
   
    while(numOfImages<=len(paths)-1):
        path = paths[numOfImages]
        numOfImages=numOfImages+1
        path2 = paths[numOfImages]
        numOfImages=numOfImages+1
        #Reset the while loop
        if(numOfImages >= len(paths)):# if total is 5 pic, 1st loop 0 > 6 /reset the loop
            numOfImages=0
            
            
            
        
        canvas = Canvas(window,width=scr_w/2, height=scr_h, bg='black')
        canvas2 = Canvas(window,width=scr_w/2, height=scr_h, bg='black')
        #gird plays the canvas without it the canvas will not work
        canvas.grid(row=0,column=0)
        canvas2.grid(row=0, column = 1)
        
        img = get_img_fit_size(path, scr_w/2, scr_h,False)
        img2 = get_img_fit_size(path2, scr_w/2, scr_h,False)
        
        my_image = canvas.create_image(int(scr_w/4),int(scr_h/2),anchor=CENTER, image=img)
        my_image_2 = canvas2.create_image(int(scr_w/4),int(scr_h/2),anchor=CENTER, image=img2)
        
        window.update()
        time.sleep(timeSleep)
        
    window.mainloop()
    
    
def Multi_view_rotate():
    global timeSleep
    timeSleep = int(timeSleep.get())
    #geting director from user input
    #directory = filedialog.askdirectory()
    directory = r"C:\Users\DotNet\Desktop\Ragazinana Data reduced\diashow\4 Random\Portrait"
    #Get paths
    paths = get_image_paths(directory)
    #read the image 
    #call the function to get the picture object with new size
    global numOfImages
    #footer path
    footerPath = r"C:\Users\DotNet\Desktop\Ragazinana Data reduced\diashow\ragaziana_s.jpg"
   
    while(numOfImages<=len(paths)-1 ):
        path = paths[numOfImages]
        numOfImages=numOfImages+1
        path2 = paths[numOfImages]
        numOfImages=numOfImages+1
        #if the next photo is out of bound then assign it to the first index
        if(numOfImages >= len(paths)):# if total is 5 pic, 1st loop 0 > 6 /reset the loop   
            numOfImages=0
    
            
            
        # each image will take 45% of the screen width
        per_w_imgs = cal_per_num(90, scr_w)/2
        
        #Footer will take 10% of the screen width
        per_w_footer = cal_per_num(10, scr_w)
        
        canvas = Canvas(window,width=per_w_imgs, height=scr_h, bg='black', highlightthickness=0, highlightbackground="black")
        canvas2 = Canvas(window,width=per_w_imgs, height=scr_h, bg='black', highlightthickness=0, highlightbackground="black")
        canvas3 = Canvas(window,width=per_w_footer, height=scr_h, bg='black', highlightthickness=1, highlightbackground="white")
        #gird plays the canvas without it the canvas will not work
        canvas3.grid(row=0,column=0)
        canvas.grid(row=0, column = 1)
        canvas2.grid(row=0, column = 2)
        
        
        
        #in order to make the picture fit in the rotated state in the half of the screen
        # we make the get_img_fit_size adjust it to us to that size by providing 
        # screen hight  as a width and half of the screen with as a height
        img = get_img_fit_size(path, scr_h, per_w_imgs, True)
        img2 = get_img_fit_size(path2, scr_h, per_w_imgs, True)
        
        #footerImg = get_img_fit_size(footerPath, scr_h, per_w_footer, True)
        footerImg1 = Image.open(footerPath)
        footerImg2 = footerImg1.transpose(Image.ROTATE_270)
        footerImg3 = footerImg2.resize((int(per_w_footer),int(scr_h)), Image.ANTIALIAS)
        footerImg = ImageTk.PhotoImage(footerImg3)
        
        
        my_image = canvas.create_image(int(scr_w/4.5),int(scr_h/2),anchor=CENTER, image=img)
        my_image_2 = canvas2.create_image(int(scr_w/4.5),int(scr_h/2),anchor=CENTER, image=img2)
        
        footer = canvas3.create_image(per_w_footer/2,scr_h/2,anchor=CENTER, image=footerImg)
        
        window.update()
        time.sleep(timeSleep)
        
    window.mainloop()
    
    
    

L1 = Label(window, text="time (Seconds)")
L1.grid(row=0, column=0)

timeSleep = tkinter.Entry(window)
timeSleep.grid(row=0, column=1)

button=Button(window,text="Single View",width=30,command=Single_view)
button.place(relx=0.2, rely=0.5, anchor=CENTER)
button2=Button(window,text="Multi Horezantal View",width=30,command=Multi_view)
button2.place(relx=0.5, rely=0.5, anchor=CENTER)
button2=Button(window,text="Multi Rotated View",width=30,command=Multi_view_rotate)
button2.place(relx=0.7, rely=0.5, anchor=CENTER)

#Full Screen keys
window.bind('<Escape>', fullScreen)
window.bind('<KP_Enter>', fullScreen)
window.bind('<Double 1>', fullScreen)


window.mainloop()


