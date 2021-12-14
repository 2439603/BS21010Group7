'''
To make this program we use some extra Python libraries called "Open CV" that allows us to use artificial vision in real time.
We want to recognise an object based on its colour in the most precise way and to verify its effectiveness.
The most important things of this software are the recognition of the edges of the object without clashing and the opening of some windows that show step by step the program.
'''
#Import the libraries, you might need to install openCV(cv2) and imutils in advanced.
#The process is given in How-to-install-OpenCV.txt in our repository.
import numpy as np
import cv2
import imutils

def recogniseColour(): #This function can identify a specific color in the image:
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #Colour space is converted from BGR(blue,green,red) to HSV(hue,saturation,value).
    #HSV express colour more intuitively for users.

    #Green colour:
    lower = np.array([36, 0, 0], np.uint8)
    upper = np.array([85, 255, 255], np.uint8)
    #Combine vector proccessing from numpy and colour model from cv2 (uint8 is a data type means brightness 0-255)
    #so colour in a blur range could be presented as intervals.
    
    #Mask and display of various image:
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("res", res)
#Mask covers areas for shape, with bitwise_and() we gain interested arrays.  
#Result in only green figures shown in res window.

def outlineRec():#Again we identify green colour, but for the object edges this time.
    lower = np.array([36, 0, 100])
    upper = np.array([85, 0, 255])
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations = 5)
    #Erosion is used to erase the unwanted digits, in this function computer excludes all that's not green.
    cv2.imshow("original", frame)
    cv2.imshow("only green", mask)
     
    #Identify the object's outline:
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    clone = frame.copy()
    #Contours means the outer edge.
    
    cv2.drawContours(clone, cnts, -1, (0, 255, 0), 2)
    print("Found {} contours".format(len(cnts)))
    
    #Centre calculation:
    for c in cnts:
        area = cv2.contourArea(c)
        if area<100:
            continue
        m = cv2.moments(c)
        if m["m00"]==0:
            continue
        cX = int(m["m10"] / m["m00"])
        cY = int(m["m01"] / m["m00"])
        cv2.circle(frame, (cX, cY), 10, (255, 0,0), -1)
        cv2.imshow("original", frame)

#Open the webcam:
cap = cv2.VideoCapture(0)
cap.set(3, 800)
cap.set(4, 600)

if not cap.isOpened():
    cap.open()
# This line helps the user to know how to end the scrpit    
print("Press Q to finish to end the script")

while(True):
    ret, frame = cap.read()

    recogniseColour()

    outlineRec()
    if cv2.waitKey(1) == ord('q'):
        break
#Waitkey is the ending code, it could be set as a time limit or key.
#Press Q to stop this program.
cap.release()
cv2.destroyAllWindows()

#Other colours for test:
'''
the values that we can find after lower and upper are call RGB number. 
The RGB color model is an additive color model[1] in which the red, green, and blue primary colours of light are added together in various ways to reproduce a broad array of colours. 
The name of the model comes from the initials of the three additive primary colours, red, green, and blue.

The main purpose of the RGB color model is for the sensing, representation, and display of images in electronic systems, such as televisions and computers, though it has also been used in conventional photography. 
Before the electronic age, the RGB color model already had a solid theory behind it, based in human perception of colours.
'''

#Orange:
#lower = np.array([5, 50, 50],np.uint8)
#upper = np.array([15, 255, 255],np.uint8)

#Blue:
#lower = np.array([110,50,50])
#upper = np.array([130,255,255])

#Red:
#lower = np.array([160, 20, 70])
#upper = np.array([190, 255, 255])

#Green (in use):
#lower = np.array([36, 0, 0], np.uint8)
#upper = np.array([85, 255, 255], np.uint8)
