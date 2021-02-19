# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 11:50:29 2021
@author: Mohammed S. Hazim
"""
import tkinter
from tkinter import *
from tkinter import colorchooser
from tkinter import ttk as ttk
from tkinter import filedialog as filedialog
import PIL
from PIL import Image, ImageTk
import os
from os import path
import time
import sys #used to accept outer arguments when running the file

#yup
#Creating tk window
window = Tk(className="Ragaziana Slide Show")
#window.iconbitmap('/home/pi/image-slider/app.ico')

#getting the screen width and hieight
scr_w = window.winfo_screenwidth()
scr_h = window.winfo_screenheight()

#making the tk window size equal to the screen size
window.geometry("700x280")

#getting list of pictures in directory
def get_image_paths(input_dir='.'):
    paths = []
    for root, dirs, files in os.walk(input_dir, topdown=True):
        for file in sorted(files):
            if file.endswith(('jpg', 'png', 'jpeg','gif')):
                path = os.path.abspath(os.path.join(root, file))
                paths.append(path)
    return paths


#function to check if the photo is landscape, portirate, or square
def imgType(path):
    imgsize = ImageTk.PhotoImage(Image.open(path))
    img_w = imgsize.width()
    img_h = imgsize.height()
    result = "none"
    if img_w > img_h:
        # l stands for landscape
        result = "l"
    elif img_h > img_w:
        # p stands for portirate
        result = "p"
    elif img_w == img_h:
        # s stands for square
        result = "s"
    else:
        pass
    return result

#Create tow lists one for landscape and one for portirate pictures
def getPaths(inputDir = '.'):
    
    global errorlabel
    portPaths = []
    landPaths = []
    for root, dirs, files in os.walk(inputDir, topdown=True):
        for file in sorted(files):
            if file.endswith(('jpg', 'png', 'jpeg','gif')):
                path = os.path.abspath(os.path.join(root, file))
                if imgType(path) == "l":
                    portPaths.append(path)
                elif imgType(path) == "p":
                    landPaths.append(path)
                elif imgType(path) == "s":
                    landPaths.append(path)
                else:
                    print("not landscape or portirate")
    return portPaths, landPaths



def get_img_fit_size(path, can_w, can_h, rotate, direction='none'):
    can_w = can_w -40;
    can_h = can_h -40;
    print("Path:", path)
    imgsize = ImageTk.PhotoImage(Image.open(path))

    # Getting 
    img_w = imgsize.width()
    img_h = imgsize.height()
    #After rotation
    img_w_r = img_h
    img_h_r = img_w
    
    # Here we resize the rotated image
    def proccess():
        # Identify if the image is Landscape, Portirate or square depending on it's original before rotating

        # Image is Landscape
        if img_w > img_h:
            # Only measure by can_h and img_h_r because it's landscape
            if img_h_r > can_h:
                nImg_h = can_h
                x = can_h/img_h_r
                nImg_w = x * img_w_r
                
            elif img_h_r <= can_h:
                nImg_h = img_h_r #Original size
                nImg_w = img_w_r #Original size
                
            
        # Image is Portirate
        elif img_w < img_h:
            # Only Measure by can_w and img_w_r because it's portirate
            if img_w_r > can_w:
                nImg_w = can_w
                x = can_w/img_w_r
                nImg_h = x * img_h_r
                
            elif img_w_r <= can_w:
                nImg_w = img_w_r #Original size
                nImg_h = img_h_r #Original size
  
        # Image is Square
        elif img_w == img_h:
            # Measuring by can_w and Img_w_r
            if img_w_r > can_w:
                nImg_w = can_w
                x= can_w/img_w_r
                nImg_h = x * img_h_r
            elif  img_w_r <= can_w:
                nImg_w = img_w_r #Original size
                nImg_h = img_h_r #Original size
                
        # Implement the size on the image
        return int(nImg_w), int(nImg_h)
###################  End proccing function #################
        
        
    # Get the image from path
    img1 = Image.open(path)
    if rotate == True:
        if direction == '90':
            #using transpose function instead of rotate to avoid cropping sides
            img2 = img1.transpose(Image.ROTATE_90)
            nImg_w, nImg_h = proccess() # Get the new size
            img3 = img2.resize((nImg_w,nImg_h), Image.ANTIALIAS) #Resizing work
            img = ImageTk.PhotoImage(img3) # to return
            print("output width:",nImg_w," Output height:", nImg_h)
            return img
            
        elif direction == '270':
            #using transpose function instead of rotate to avoid cropping sides
            img2 = img1.transpose(Image.ROTATE_270)
            nImg_w, nImg_h = proccess() # Get the new size
            
            img3 = img2.resize((nImg_w,nImg_h), Image.ANTIALIAS) #Resizing work
            img = ImageTk.PhotoImage(img3) # to return
            return img
        else:
            print("wrong argument for direction of rotation")
            return None
            
    else:
        print("Not rotated")
        return None
    
    
    

#function inputs percentage and number and outputs how much is that percentage in the number
def cal_per_num(percentage, number):
    quotient = percentage / 100
    percentage = quotient * number
    return percentage


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
       

#Our global variable, increase it in the global scope, not only inside the functions
numOfImages = 0
numOfImagesPort=0 
numOfImagesLand=0

def oldCommented():
    
    # =============================================================================
    # def Single_view(timeSleep,directory,colorEntry):
    #     window.geometry(str(scr_w)+"x"+str(scr_h)+"+0+0")
    #     window.attributes('-fullscreen', True)
    #     
    #     
    #     #directory = allDirEntry.get()
    #     #directory = r"C:\Users\DotNet\Desktop\Ragazinana Data reduced\diashow\4 Random\Portrait"
    #     #Get paths
    #     paths = get_image_paths(directory)
    #     #read the image 
    #     #call the function to get the picture object with new size
    #     global numOfImages
    #     
    #     path = paths[numOfImages]
    #     
    #     while(numOfImages<=len(paths)-1):#if total is 5 pictures then 1st loop 0 <= 6-1 ==> 0 <= 5 ,2nd loop 1 <= 5
    #         
    #         path = paths[numOfImages]
    #         numOfImages=numOfImages+1
    #         
    #         if(numOfImages>len(paths)):# if total is 5 pic, 1st loop 0 > 6 /reset the loop
    #             numOfImages=0 
    #         
    #         
    #         #createing canvas and make it equal to the screen width and hight
    #         canvas = Canvas(window,width=scr_w, height=scr_h, bg=bgcolor)
    #         #gird plays the canvas without it the canvas will not work
    #         canvas.grid(row=0,column=0)
    #         
    #         
    #         
    #         img = get_img_fit_size(path, scr_w, scr_h, False)
    #         my_image = canvas.create_image(int(scr_w/2),int(scr_h/2),anchor=CENTER, image=img)
    #         
    #         
    #         #Text View
    #         path_arr = path.split("\\") # split the direcoties of the image path 
    #         f_img = (path_arr[-1]) # get the last index of the array of the path
    #         result = f_img[:-4] # Remve last characters from the image name
    #         description = result
    #     
    #         my_regtangle = canvas.create_rectangle(scr_w/2-250,scr_h/1.15-20,scr_w/2+250,scr_h/1.15+20,fill="black")
    #         
    #         my_message = canvas.create_text(scr_w/2,scr_h/1.15,fill="#fff",font="family",text=description,anchor="center")
    #         window.update()
    #         time.sleep(timeSleep)
    #     
    #     window.mainloop()
    #     
    # def Multi_view():
    #     window.geometry(str(scr_w)+"x"+str(scr_h)+"+0+0")
    #     window.attributes('-fullscreen', True)
    #     
    #     global timeSleep
    #     timeSleep = int(timeSleep.get())
    #     global colorEntry
    #     bgcolor = colorEntry.get()
    #     
    #     #Getting Directory from user input
    #     directory = allDirEntry.get()
    #     #directory = r"C:\Users\DotNet\Desktop\Ragazinana Data reduced\diashow\4 Random\Portrait"
    #     #Get paths
    #     paths = get_image_paths(directory)
    #     #read the image 
    #     #call the function to get the picture object with new size
    #     global numOfImages
    #     
    #    
    #     while(numOfImages<=len(paths)-1):
    #         path = paths[numOfImages]
    #         numOfImages=numOfImages+1
    #         
    #         #Reset the while loop
    #         if(numOfImages >= len(paths)):# if total is 5 pic, 1st loop 0 > 6 /reset the loop
    #             numOfImages=0
    #             continue 
    #         path2 = paths[numOfImages]
    #         numOfImages=numOfImages+1
    #             
    #             
    #         
    #         canvas = Canvas(window,width=scr_w/2, height=scr_h, bg=bgcolor)
    #         canvas2 = Canvas(window,width=scr_w/2, height=scr_h, bg=bgcolor)
    #         #gird plays the canvas without it the canvas will not work
    #         canvas.grid(row=0,column=0)
    #         canvas2.grid(row=0, column = 1)
    #         
    #         img = get_img_fit_size(path, scr_w/2, scr_h,False)
    #         img2 = get_img_fit_size(path2, scr_w/2, scr_h,False)
    #         
    #         my_image = canvas.create_image(int(scr_w/4),int(scr_h/2),anchor=CENTER, image=img)
    #         my_image_2 = canvas2.create_image(int(scr_w/4),int(scr_h/2),anchor=CENTER, image=img2)
    #         
    #         window.update()
    #         time.sleep(timeSleep)
    #         
    #     window.mainloop()
    #     
    # =============================================================================
    pass
    
def Multi_view_rotate_270(timeSleepVal,footerPath,bgcolor,pathsPrt,pathsLand):
    
    print("-90 (270) view");
    #Creating tk window
    window.attributes('-fullscreen', True)
    window.geometry(str(scr_w)+"x"+str(scr_h)+"+0+0")
    window.configure(bg=bgcolor)
    
    #Setup the direction of the rotation
    direction = "270"

    #read the image 
    #call the function to get the picture object with new size
    global numOfImagesPort
    global numOfImagesLand
    #footer path
    #footerPath = "C:/Users/DotNet/Desktop/Ragazinana Data reduced/diashow/ragaziana_s.jpg"
    
    #Footer will take 8% of the screen width   
    per_w_footer = cal_per_num(8, scr_w)
    # Footer Image operations
    canvasFoot = Canvas(window,width=per_w_footer, height=scr_h, bg=bgcolor, highlightthickness=1, highlightbackground=bgcolor)
    canvasFoot.grid(row=0, column=0)

    
    #footerImg = get_img_fit_size(footerPath, scr_h, per_w_footer, True)
    footerImg1 = Image.open(footerPath)
    footerImg2 = footerImg1.transpose(Image.ROTATE_270)
    footerImg3 = footerImg2.resize((int(per_w_footer),int(scr_h)), Image.ANTIALIAS)
    footerImg = ImageTk.PhotoImage(footerImg3)
    footer = canvasFoot.create_image(per_w_footer/2,scr_h/2,anchor=CENTER, image=footerImg)
    
    
    while(numOfImagesPort<=len(pathsPrt)-1 or numOfImagesLand<=len(pathsLand)-1 ):
        
        pathPort = pathsPrt[numOfImagesPort]
        #increase the index to get the next file in the next loop
        numOfImagesPort=numOfImagesPort+1
        #if the next photo is out of bound then assign it to the first index
        if(numOfImagesPort >= len(pathsPrt)):# if total is 5 pic, 1st loop 0 > 6 /reset the loop   
            numOfImagesPort=0
            
        # each image will take as following in percentage
        per_w_imgs_portriate = cal_per_num(42, scr_w)
        per_w_imgs_landscape= cal_per_num(50, scr_w)

        #Create the canvases
        canvasPort = Canvas(window,width=per_w_imgs_portriate, height=scr_h, bg=bgcolor, highlightthickness=10, highlightbackground=bgcolor)
        
        #gird plays the canvas without it the canvas will not work
        canvasPort.grid(row=0, column=1)

        #in order to make the picture fit in the rotated state in the half of the screen
        # we make the get_img_fit_size adjust it to us to that size by providing 
        # screen hight  as a width and half of the screen with as a height
        imgPort = get_img_fit_size(pathPort, scr_h, per_w_imgs_portriate, True, direction)
        
        portImgCanvas = canvasPort.create_image(int(scr_w/4.3),int(scr_h/2),anchor=CENTER, image=imgPort)
        canvasPort.move(portImgCanvas, 0, -200)
        window.update()
        count, x, y = 0, 0 ,0
        while count < 90:
            y += 0.05
            canvasPort.move(portImgCanvas, x, y)
            time.sleep(0.01)
            window.update()
            count += 1
            
    
        time.sleep(timeSleepVal/2)
        
        # Landscape image 
        pathLand = pathsLand[numOfImagesLand]
        numOfImagesLand = numOfImagesLand+1
        
        if(numOfImagesLand >= len(pathsLand)):
            numOfImagesLand=0
            
        
        canvasLand = Canvas(window,width=per_w_imgs_landscape, height=scr_h, bg=bgcolor, highlightthickness=10, highlightbackground=bgcolor)
        canvasLand.grid(row=0, column=2)
        imgLand = get_img_fit_size(pathLand, scr_h, per_w_imgs_landscape, True,direction)
        landImgCanvas = canvasLand.create_image(int(scr_w/4.5),int(scr_h/2),anchor=CENTER, image=imgLand)
        
        canvasLand.move(landImgCanvas, 0, -200)
        window.update()
        count2, x2, y2 = 0, 0 ,0
        while count2 < 90:
            y2 += 0.05
            canvasLand.move(landImgCanvas, x2, y2)
            time.sleep(0.01)
            window.update()
            count2 += 1
            
        window.update()
        time.sleep(timeSleepVal/2)
        
    window.mainloop()

def Multi_view_rotate_90(timeSleepVal,footerPath,bgcolor,pathsPrt,pathsLand):
    print("90 View")
        #Creating tk window
    window.attributes('-fullscreen', True)
    window.geometry(str(scr_w)+"x"+str(scr_h)+"+0+0")
    window.configure(bg=bgcolor)
    
    #direction
    direction = "90"
    #read the image 
    #call the function to get the picture object with new size
    global numOfImagesPort
    global numOfImagesLand
    #footer path
    #footerPath = "C:/Users/DotNet/Desktop/Ragazinana Data reduced/diashow/ragaziana_s.jpg"
    
    #Footer will take 8% of the screen width   
    per_w_footer = cal_per_num(8, scr_w)
    # Footer Image operations
    canvasFoot = Canvas(window,width=per_w_footer, height=scr_h, bg=bgcolor, highlightthickness=2, highlightbackground=bgcolor)
    canvasFoot.grid(row=0, column=2)

    
    #footerImg = get_img_fit_size(footerPath, scr_h, per_w_footer, True)
    footerImg1 = Image.open(footerPath)
    footerImg2 = footerImg1.transpose(Image.ROTATE_90)
    footerImg3 = footerImg2.resize((int(per_w_footer),int(scr_h)), Image.ANTIALIAS)
    footerImg = ImageTk.PhotoImage(footerImg3)
    footer = canvasFoot.create_image(per_w_footer/2,scr_h/2,anchor=CENTER, image=footerImg)
    
    # each image will take as following in percentage
    per_w_imgs_portriate = cal_per_num(50, scr_w) #outputs pixels of 50% of the provided pixles
    per_w_imgs_landscape= cal_per_num(42, scr_w) #outputs pixels of 42% of the provided pixles
    print('per_w_imgs_portriate:',per_w_imgs_portriate, ' per_w_imgs_landscape:',per_w_imgs_landscape)
    
    while(numOfImagesPort<=len(pathsPrt)-1 or numOfImagesLand<=len(pathsLand)-1 ):
        
        pathPort = pathsPrt[numOfImagesPort]
        #increase the index to get the next file in the next loop
        numOfImagesPort=numOfImagesPort+1
        #if the next photo is out of bound then assign it to the first index
        if(numOfImagesPort >= len(pathsPrt)):# if total is 5 pic, 1st loop 0 > 6 /reset the loop   
            numOfImagesPort=0
            
        can_w_l = per_w_imgs_portriate
        can_h_l = scr_h
        
        # Create the canvases
        canvasPort = Canvas(window,width=can_w_l, height=can_h_l, bg=bgcolor, highlightthickness=1, highlightbackground=bgcolor)
        
        # Gird plays the canvas without it the canvas will not work
        canvasPort.grid(row=0, column=0)
        
        

        # Because the image will be rotated then resized in get_img_fit_size method and user these valus
        # After it's completly rotated then we give the canvas width and heigt
        imgPort = get_img_fit_size(pathPort, can_w_l, can_h_l, True, direction)
        
        # In order to make the picture fit in the rotated state in the half of the screen
        # we make the get_img_fit_size adjust it to us to that size by providing 
        # screen hight  as a width and half of the screen with as a height
        portImgCanvas = canvasPort.create_image(int(scr_w/4.3),int(scr_h/2),anchor=CENTER, image=imgPort)
        canvasPort.move(portImgCanvas, 0, -200)
        window.update()
        count, x, y = 0, 0 ,0
        while count < 90:
            y += 0.05
            canvasPort.move(portImgCanvas, x, y)
            time.sleep(0.01)
            window.update()
            count += 1
                    
        # Brake between the pictures view
        time.sleep(timeSleepVal/2)
        
        # Landscape image 
        pathLand = pathsLand[numOfImagesLand]
        numOfImagesLand = numOfImagesLand+1
        
        if(numOfImagesLand >= len(pathsLand)):
            numOfImagesLand=0
        
        #defining canvas width and height
        can_w_l = per_w_imgs_landscape
        can_h_l = scr_h
        
        
        
        canvasLand = Canvas(window,width=can_w_l, height=can_h_l, bg=bgcolor, highlightthickness=1, highlightbackground=bgcolor)
        canvasLand.grid(row=0, column=1)
        imgLand = get_img_fit_size(pathLand, can_w_l, can_h_l, True, direction)
        landImgCanvas = canvasLand.create_image(0,0,anchor=NW, image=imgLand)
        
        canvasLand.move(landImgCanvas, 0, -200)
        window.update()
        count2, x2, y2 = 0, 0 ,0
        while count2 < 95:
            y2 += 0.05
            canvasLand.move(landImgCanvas, x2, y2)
            time.sleep(0.01)
            window.update()
            count2 += 1
            
        window.update()
        time.sleep(timeSleepVal/2)
        
    window.mainloop()
# This Function is for creating new config file
def createFile():
    fileWrite=open("config",'w+')
# This Function is for Replaceing content with a value to the config file
def insertValue(value):
    fileWrite=open("config",'w+')
    fileWrite.write(value)
    fileWrite.close()
#This function runs when the check box is checked
def checkBoxReboot():
    #Check the Checkbox if it's checked or not
    global chk
    chkArr = chk.state()
    if chkArr[2] == "selected":
        print("The chekc box is selected")
        createFile()
        insertValue("True")
    else:
        print("The CheckBox is Not Selected")
        createFile()
        insertValue("False")
#       
def startOnReboot():
    #Check the Checkbox if it's checked or not
    global chk
    chkArr = chk.state()
    if chkArr[-1] == "selected":
        print("The chekc box is selected")
        createFile()
        insertValue("True")
    else:
        print("The CheckBox is Not Selected")
        createFile()
        insertValue("False")
    
def close(event):
    window.destroy()
def hide_me(event):
    event.widget.grid_forget()    

#function to insert the footer file neme to the text input
def insert():
    file = filedialog.askopenfilename()
    global footerPath
    footerPath.delete(0, 'end')
    footerPath.insert(0,file)
def insertAllDir():
    file = filedialog.askdirectory()
    global allDirEntry
    allDirEntry.delete(0, 'end')
    allDirEntry.insert(0, file)
def insertPortDir():
    file = filedialog.askdirectory()
    global portDirEntry
    portDirEntry.delete(0, 'end')
    portDirEntry.insert(0, file)
def insertLandDir():
    file = filedialog.askdirectory()
    global landDirEntry
    landDirEntry.delete(0, 'end')
    landDirEntry.insert(0, file)
    
     
def choose_color():
    global colorEntry
    # variable to store hexadecimal code of color
    color_code = tkinter.colorchooser.askcolor(title ="Choose color")

    #insert color code to the text box
    colorEntry.delete(0, 'end')
    colorEntry.insert(0, color_code[1])
    colorEntry.config({"background": colorEntry.get()})
    
def toggle():
    globals()
    
    if folderMode.config('relief')[-1] == 'sunken':
        
        # Show Single folder inputs
        L3.grid(row=2, column=0,pady=5, padx=20)
        allDirEntry.grid(row=2, column=1)
        #Hid multiple folders input
        L3Port.grid_forget()
        L3Land.grid_forget()
        portDirEntry.grid_forget()
        landDirEntry.grid_forget()
        port_btn.grid_forget()
        land_btn.grid_forget()
        #Enable Single view choice
        #choice1.configure(state = NORMAL)

        all_btn.grid(row=2, column=2,pady=5, padx=20)
        folderMode.config(relief="raised")
        folderMode.configure(bg='white')
        
        
    else:
        #hide single folder input 
        L3.grid_forget()
        allDirEntry.grid_forget()
        all_btn.grid_forget()
        # Show multiple folders inputs
        L3Port.grid(row=2, column=0,pady=5, padx=20)
        L3Land.grid(row=3, column=0,pady=5, padx=20)
        portDirEntry.grid(row=2, column=1)
        landDirEntry.grid(row=3, column=1)
        port_btn.grid(row=2, column=2,pady=5, padx=20)
        land_btn.grid(row=3, column=2,pady=5, padx=20)
        #Disable Single view choice
        #choice1.configure(state = DISABLED)
        
        folderMode.config(relief="sunken")
        folderMode.configure(bg='#65fe5c')
        
        
        

# Check all inputs before procceding to the main functoin

def checkPlay(mode="none"):
    
    globals()
    allDirEntryVal = allDirEntry.get() #getting folder path from input
    portDirEntryVal = portDirEntry.get() #getting folder path from input
    landDirEntryVal = landDirEntry.get() #getting folder path from input
    
    #When the user on single folder mode
    if folderMode.config('relief')[-1] == 'raised' and mode=="none":
        #using allPaths function
        allPaths = getPaths(allDirEntryVal) #sending it to the function to seperate and return multi dimention array
        pathsPrt = allPaths[0] #potirate paths
        pathsLand = allPaths[1] #landscape  pahes
    # When the user on Multi folder mode or it recives the mode parameter
    if folderMode.config('relief')[-1] == 'sunken' or mode=="multi":
        #Something is wrong with swapping, accourding to the testing I should replace them
        pathsPrt = get_image_paths(portDirEntryVal)
        pathsLand = get_image_paths(landDirEntryVal)

    
    
    #print ("resurt", Radio_Value0.get ())
    #print(timeSleep.get(), colorEntry.get(),footerPath.get(),allDirEntry.get())
    if timeSleep.get() != "" and colorEntry.get() != "" and footerPath.get() != "" and (allDirEntry.get() != "" or (portDirEntry.get() != "" and landDirEntry.get() != "")):
        # Storing input values to variables
        timeSleepVal = int(timeSleep.get())
        footerPathVal = footerPath.get()
        #geting director from entry boxes
        
        bgcolorVal = colorEntry.get()
        
        
        #Removing all input elements
        L1.destroy()
        L2.destroy()
        L3.destroy()
        L4.destroy()
        timeSleep.destroy()
        footerPath.destroy()
        colorEntry.destroy()
        select_btn.destroy()
        all_btn.destroy()
        colorButton.destroy()
        radioGroup.destroy()
        button3.destroy()
        
        #Single_view(timeSleepVal,allDirEntryVal,bgcolorVal)
        if Radio_Value0.get () == 0:
            Multi_view_rotate_90(timeSleepVal,footerPathVal,bgcolorVal,pathsPrt,pathsLand)
        elif Radio_Value0.get () == 1:
            Multi_view_rotate_270(timeSleepVal,footerPathVal,bgcolorVal,pathsPrt,pathsLand)
        else:
            error.configure(text="Something went wrong while detectig the view mode type")
            error.grid(row=7, column=1)
    else:
        error.configure(text="Please make sure to all fields are selected!")
        error.grid(row=7, column=1)
        
        


error = Label(window, text="Error",fg="red")

L1 = Label(window, text="Time (Seconds)")
L1.grid(row=0, column=0,pady=5, padx=20)

L2 = Label(window, text="Footer photo Path")
L2.grid(row=1, column=0,pady=5, padx=20)

L3 = Label(window, text="Pictures Folder")
L3.grid(row=2, column=0,pady=5, padx=20)

L3Port = Label(window, text="Portrait Folder")
#L3Port.grid(row=2, column=0,pady=5, padx=20)


L3Land = Label(window, text="Landscape Folder")
#L3Land.grid(row=3, column=0,pady=5, padx=20)

L4 = Label(window, text="Background color")
L4.grid(row=5, column=0,pady=5, padx=20)

timeSleep = tkinter.Entry(window)
timeSleep.insert(0, "10")
#timeSleep.insert(0, "1")
timeSleep.grid(row=0, column=1)



footerPath = tkinter.Entry(window,width=50)
footerPath.insert(0, "/home/pi/Desktop/diashow//ragaziana_s.jpg")
#footerPath.insert(0, "C:/Users/DotNet/Desktop/diashow/ragaziana_s.jpg")
footerPath.grid(row=1, column=1)

allDirEntry = tkinter.Entry(window,width=50)
allDirEntry.insert(0, "")
allDirEntry.grid(row=2, column=1)

portDirEntry = tkinter.Entry(window,width=50)
portDirEntry.insert(0, "/home/pi/Desktop/diashow/4 Random/Portrait")
#portDirEntry.insert(0, "C:/Users/DotNet/Desktop/diashow/4 Random/Portrait")
#portDirEntry.grid(row=2, column=1)

landDirEntry = tkinter.Entry(window,width=50)
landDirEntry.insert(0, "/home/pi/Desktop/diashow/4 Random/Landschaft")
#landDirEntry.insert(0, "C:/Users/DotNet/Desktop/diashow/4 Random/Landschaft")

#landDirEntry.grid(row=3, column=1)

colorEntry = tkinter.Entry(window, width=50)
colorEntry.insert(0, "#ffffff")
colorEntry.grid(row=5, column=1)

select_btn = Button(window,text="Select file",width=10,command=insert)
select_btn.grid(row=1, column=2,pady=5, padx=20)

all_btn = Button(window,text="Select Folder",width=10,command=insertAllDir)
all_btn.grid(row=2, column=2,pady=5, padx=20)

port_btn = Button(window,text="Select Folder",width=10,command=insertPortDir)
#port_btn.grid(row=2, column=2,pady=5, padx=20)

land_btn = Button(window,text="Select Folder",width=10,command=insertLandDir)
#land_btn.grid(row=3, column=2,pady=5, padx=20)



folderMode = tkinter.Button(text="2 Folders Mode", width=12, relief="raised", command=toggle)
folderMode.grid(row=6, column=0)

colorButton = Button(window, text = "Select color",command = choose_color, width=10)
colorButton.grid(row=5, column=2,pady=5, padx=20)

radioGroup = LabelFrame(window, text = "Select view type")
radioGroup.grid(row=6, column=1)

#Varibale to use in choices
Radio_Value0 = tkinter.IntVar ()
Radio_Value0.set(0)
#Select view mode
# =============================================================================
# choice1 = ttk.Radiobutton(radioGroup, text="Single View", variable = Radio_Value0, value = not yet)
# choice1.configure(state = DISABLED)
# choice1.grid(row=6, column=0)
# choice2 = ttk.Radiobutton(radioGroup, text="Multi View", variable = Radio_Value0, value = not yet)
# choice2.configure(state = DISABLED)
# choice2.grid(row=6, column=1)
# =============================================================================
choice3 = ttk.Radiobutton(radioGroup, text="Standard", variable = Radio_Value0, value = 0)
choice3.grid(row=6, column=2)
choice3 = ttk.Radiobutton(radioGroup, text="Rotate", variable = Radio_Value0, value = 1)
choice3.grid(row=6, column=3)


#chk = ttk.Checkbutton(window, text="Start Slideshow on Reboot", command=checkBoxReboot)
#chk.grid(row=7, column=0)




button3=Button(window,text="Play",width=10,command=checkPlay, bg='#d5eaff')
#button3.place(relx=0.7, rely=0.5, anchor=CENTER)
button3.grid(row=6, column=2,pady=20, padx=20)
#Full Screen keys
window.bind('<Escape>', close)
window.bind('<Double 1>', fullScreen)

# This function returns True if config file content is True, False if next


#Check if config file is exists if it's not exists Create new one
#Change the state of the checkbox accourign to the file state
# =============================================================================
# if path.exists("config"):
#     print("File is already Exists")
#     # Chack if config has True or false vlaue
#     file=open("config",'r')
#     chkValue=file.readline()
#     #Setup the Checkbox state Accourding to the content of the file
#     if chkValue == "True":
#         # Check the box if the state was enable
#         CheckVar = IntVar()
#         CheckVar.set(1)
#         chk.configure(variable = CheckVar)
#         print("State is Normal")
#         
#     else:
#         # Uncheck the box if the state was 
#         CheckVar = IntVar()
#         CheckVar.set(0)
#         chk.configure(variable = CheckVar)
#         print("State is Disabled") 
#         
# else:
#     #Create file and set it up on True
#     createFile()
#     insertValue("False")
#     print("File Have been created successfuly!")
# =============================================================================

#Getting the requested 
def readFileLine(line):
    with open("config", "r") as text_file:
        data = text_file.readlines()
        return data[line]


#When getting outer paramater 
#print("what we have got",readFileLine(0))
try:
    print(str(sys.argv[1]))
    if str(sys.argv[1]) == "auto_run":#When incomming parameter is auto_run and file input is True
        checkPlay("multi")
        
except:
    pass

# Toggle the mode to be the default view to the program on starup
toggle()

window.mainloop()

