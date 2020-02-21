# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 23:42:52 2020

@author: justi
"""


import cv2 as cv
import numpy as np
import math
import serial as sl

def main():
    #read fr
    cap = cv.VideoCapture(0)  
    while True:
        _, frame = cap.read()
        blurred_frame = cv.GaussianBlur(frame,(5,5),0)
        hsv = cv.cvtColor(blurred_frame,cv.COLOR_BGR2HSV)
        lower_blue = np.array([60,50,50])
        upper_blue = np.array([130,255,255])
        mask = cv.inRange(hsv,lower_blue,upper_blue)
        res = cv.bitwise_and(frame,frame, mask = mask)
        contours,_ = cv.findContours(mask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        top_left,top_right,bottom_left,bottom_right = None,None,None,None
        centre = None
        
        #keep creating contours until a blue rectangle is located, 
        #then use the vertices of the rectanglet to guage position and move accordingly
        for cnt in contours:
            area = cv.contourArea(cnt)
           
            approx = cv.approxPolyDP(cnt,0.02*cv.arcLength(cnt,True),True)
          
            #ignore objects which do not have 4 sides, and are too small to be the tape box
            if(len(approx) == 4) and (area>200):
                perim = cv.arcLength(approx, True)
                cv.drawContours(frame, [approx], -1, (0,225,0),3)
                vertices = classify(approx)
                #classify will return false if the contour argument is not a rectangle
                if(vertices!=False):
                    top_left,top_right,bottom_left,bottom_right = classify(approx)
                    #find the centre of the rectangular contour, then move the robot until
                    #the centre of the box is in the desired position
                    centre = getCentre(top_left, top_right, bottom_left, bottom_right)
                    move(centre)   
                    break
               
    
    
        cv.imshow("Frame", frame)
        cv.imshow("res",res)
    
        key = cv.waitKey(1)
        if key == 27: #this is the escape key
            break
            

    cap.release()
    cv.destroyAllWindows()
    
    
def classify(sides):
    if (len(sides) != 4):
        print("this is not a rectangle")
        return False
    #print("sides is " + str(sides))
    vertices = []
    xCords = []
    yCords = []
    top = []
    bot = []
    #deconstruct the nd-array into a list of 2 element arrays
    for i in sides:
        #print("i is " + str(i))
        vertices = vertices + [i[0]]
        xCords = xCords + [i[0][0]]
        yCords = yCords + [i[0][1]]
        #print("vertices is now" + str(vertices))
        
    #print(vertices[0][0])
    
    xMax = max(xCords)
    yMax = max(yCords)

    for j in vertices:
        if(abs(j[1] -yMax)<3 ):
            top = top + [j]
        else:
            bot = bot + [j]
            
    print(top)
    print(bot)
    if(len(top)!=2 or len(bot)!=2):
        return False
    if(top[0][0]>top[1][0]):
        top_left = top[1]
        top_right = top[0]
    else:
        top_left = top[0]
        top_right = top[1]
        
    if(bot[0][1]>bot[1][1]):
        bottom_left = bot[1]
        bottom_right = bot[0]
    else:    
         bottom_left = bot[0]
         bottom_right = bot[1]
        
    return [top_left,top_right,bottom_left,bottom_right]


#assumes the shape is a perfect rectangle
def getCentre(top_left,top_right,bottom_left,bottom_right):

    x = (top_left[0] + top_right[0])/2
    y = (top_left[1] + bottom_left[1])/2
    return [x,y]

def move(centre):
    #nothing here rn
    return None
  
    
main()