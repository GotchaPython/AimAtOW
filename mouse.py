#!/usr/bin/python
import sys
import inspect
import hack
import win32ui
import requests
import getpass
import zipfile, StringIO
#IMPORTS
from PIL import ImageGrab
import numpy as np
import cv2
import ctypes
import pyautogui
from math import sqrt
import win32gui, win32con,win32api,pywintypes
import Tkinter
import thread
import time

MOUSEEVENTF_MOVE = 0x0001 # mouse move
MOUSEEVENTF_ABSOLUTE = 0x8000 # absolute move
MOUSEEVENTF_MOVEABS = MOUSEEVENTF_MOVE + MOUSEEVENTF_ABSOLUTE #less typing later
MOUSE_LEFTDOWN = 0x0002     # left button down 
MOUSE_LEFTUP = 0x0004       # left button up
MOUSE_CLICK = MOUSE_LEFTDOWN + MOUSE_LEFTUP


screenWidth, screenHeight = pyautogui.size() #Screen Size/Resolution
centerwidth = screenWidth/2 #gets middle screen
centerheight = screenHeight/2 #gets middle screen

def aimactivate():
    label = Tkinter.Label(text='Aimbot Activated', font=('Times New Roman','20'), fg='Blue', bg='white')
    label.master.overrideredirect(True)
    label.master.geometry("+20+50")
    label.master.lift()
    label.master.wm_attributes("-topmost", True)
    label.master.wm_attributes("-disabled", True)
    label.master.wm_attributes("-transparentcolor", "white")

    hWindow = pywintypes.HANDLE(int(label.master.frame(), 16))
    # http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
    # The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
    exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
    win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)

    label.pack()
    label.mainloop()

def aiminside():
#loops forever, never gives up. 
    while(True):
        time.sleep(0.1)
        global currentMouseX
        global currentMouseY
        currentMouseX, currentMouseY = pyautogui.position()
    ##parameters for cropping the image, not really necessary but not much reason to work on the entire screenshot. 
    ##This probably has to be tweaked for the individual so you're capturing the area around the center of the screen. 
        CROP_LEFT = (centerwidth - 160)
        CROP_RIGHT = (centerwidth + 240) 
        CROP_TOP = (centerheight - 190)
        CROP_BOTTOM = (centerheight + 60)
     
    ##range of blue color in HSV. 
    ##Why BLUE and not RED for the outline?? Well, the original image is RGB but opencv uses BGR. 
    ##Since red is wrapped around 0 Hue in HSV format it's actually just easier to keep it in BGR and find blue outline instead of doing two masks for red. 
        lower_blue = np.array([115,100,120])
        upper_blue = np.array([130,255,255])
        
        
        
        
    #grabs the entire screen
        img = ImageGrab.grab()
     
    #convert PIL image to numpy array
        img_np = np.array(img) 
     
    #crop the image so we're not wasting time. It's just a numpy array so we can chop it like this. 
        cropped = img_np[CROP_TOP:CROP_BOTTOM, CROP_LEFT:CROP_RIGHT]
     
     
    #convert image to HSV
        img_hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV) 
     
     
    #Threshold the HSV image to get only blue colors. Really finding the red colors in an RGB image. 
        mask = cv2.inRange(img_hsv, lower_blue, upper_blue) 
     
     
    #Bitwise-AND the mask and original image for fun. for debugging.
        #res = cv2.bitwise_and(cropped,cropped, mask= mask)    
     
    #find contours
        _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  
    #list to hold all areas. 
        areas = [] 
        for contour in contours:
            ar = cv2.contourArea(contour)
            areas.append(ar)
        if len(areas) == 0:
            print("[-] No area found!")
        else:
            max_area = max( areas )
            max_area_index = areas.index(max_area)
     
    #largest area contour
            lrgst_cnt = contours[max_area_index] 
     
     #draw contour only on largest contour, commented out because it was for debugging. 
        #cv2.drawContours(cropped, [lrgst_cnt], 0, (128,255,0), 2, maxLevel = 0)
     
    #find a bounding circle on the largest contour
            (cx,cy),radius = cv2.minEnclosingCircle(lrgst_cnt) 
         
        #draw circle in red color
            cv2.circle(cropped,(int(cx),int(cy)),int(radius),(0,0,255),2)   
            
        #to get the "true" center we have to add our cropped pixels.
            global center_x
            global center_y
            center_x = int(cx)+CROP_LEFT 
            center_y = int(cy)+CROP_TOP
            #print("[-] Position Locked: ({0}, {1})".format(int(center_x),int(center_y)))

            x_good = (center_x + 0)
            y_good = (center_y + 100)
            #detect if your inside radius
            if (currentMouseX- center_x)**2 + (currentMouseY - center_y)**2 < radius**2:
                ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVEABS, center_x, center_y, 0, 0)
            k = cv2.waitKey(10)