# AUTHOR: JAUME BENSENY
#
# IMPORTANT : EXECUTION TIME IS CONTROLLER BY COUNTER WITHIN THE WHILE LOOP

import subprocess
from subprocess import check_output
from math import fabs
import re
import numpy as np
import matplotlib.pyplot as plt
import time

#returns X and Y positions of the pointer
def pointer_location ():
    aux = []
    pos = []
    out = check_output(["xdotool","getmouselocation"])
    aux = re.findall("[0-9]+", out)
    pos = map (int, aux)
    #print("TEMP POS ->", pos[0],pos[1])
    return pos

#move pointer to position X and Y
def pointer_moveto (x,y):
    subprocess.call(["xdotool","mousemove",x,y])

#estimate new position
def predict(pos,last_pos,x_lenght,y_lenght):
    global z
    global x_offset
    global y_offset
    global buffer_x
    global buffer_y
    dif_z = 0
    new_pos = pos
    cost_multiplier = 6

    #limit control
    if pos[0] > x_lenght+x_offset-2:
        pos[0] = x_lenght+x_offset-2
    if pos[1] > y_lenght-2+y_offset:
        pos[1] = y_lenght+y_offset-2
    #print("Xpos,Ypos ->", last_pos[0]-x_offset,last_pos[1]-y_offset)
    
    #difference between positions
    dif_x = pos[0] - last_pos[0]
    dif_y = pos[1] - last_pos[1]
    #print("->BX,BY",buffer_x,buffer_y)

    #check which is next pixel
    dif_z = z[pos[1]-y_offset][pos[0]-x_offset] - z[last_pos[1]-y_offset][last_pos[0]-x_offset]
    cost = fabs(dif_z)
    
    #new position calculus
    #if same height
    if dif_z== 0:
        #print("FLAT")
        return
    #if climbing up
    elif dif_z > 0:
        #print("------>UP",cost)
        if cost < fabs(buffer_x):
            new_pos[0] = pos[0]
            buffer_x = 0
        else:
            new_pos[0] = last_pos[0]
            buffer_x = buffer_x + 300 * dif_x
            
        if cost < fabs(buffer_y):
            new_pos[1] = pos[1]
            buffer_y = 0
        else:
            new_pos[1] = last_pos[1]
            buffer_y = buffer_y + 300 * dif_y
    #if getting down
    elif dif_z < 0:
        #print("-------------->DOWN")
        if dif_x > 0:
            new_pos[0] = pos[0] + 10
        elif dif_x < 0:
            new_pos[0] = pos[0] - 10
        if dif_y > 0:
            new_pos[1] = pos[1] + 10
        elif dif_y < 0:
            new_pos[1] = pos[1] - 10
        buffer_x = 0
        buffer_y = 0

    pointer_moveto(str(new_pos[0]),str(new_pos[1]))

#generate map 
x_lenght = 800
y_lenght = 600
z = np.zeros((y_lenght,x_lenght))
# specify circle parameters: centre ij and radius
ci,cj=450,300
# Create different levels of cost (hights) for each radius distance 
for i in range(150):
    cr = 149-i
    I,J=np.meshgrid(np.arange(z.shape[0]),np.arange(z.shape[1]))
    dist=np.sqrt((I-ci)**2+(J-cj)**2)
    z[np.where(dist<cr)]= pow(i+1,2)
#in case you want a print the image, uncomment following lines until show()
#fig=plt.figure()
#ax=fig.add_subplot(111)
#ax.pcolormesh(z)
#ax.set_aspect('equal')
#plt.show()

#variables
counter = 0
pos = []
new_pos = []
#buffer for accumulated pixels
buffer_x = 0
buffer_y = 0
#we open the map picture
print("*** HELLO *** ")
print("- PLEASE WAIT UNTIL THE PICTURE OPENS - ")
subprocess.call(["gnome-open","bump_final.png"])
#wait for the window to open
print("- PLEASE WAIT UNTIL THE POINTER GETS IN THE UPPER SIDE OF THE IMAGE - ")
time.sleep(3)
#we relocate mouse to point 00 of image ( upper left corner )
aux = check_output(["xdotool","search","--name","bump_final.png"])
window = re.findall("[0-9]+", aux)
#
# CONFIG TO OTHER DESKTOP CONFIGURATIONS AND MARGINS --
# Adjust the value "1" and "41" to make your pointer start at position 0,0 of the image 
#
subprocess.call(["xdotool","mousemove","--window",str(window[0]),"1","41"])
last_pos = pointer_location()
#calculte offset to match real pointer position with position in the map
x_offset = last_pos[0]
y_offset = last_pos[1]
print("- GO! GO! GO! - ")
while True:
    pos = pointer_location()
    predict(pos,last_pos,x_lenght,y_lenght)
    counter = counter + 1
    last_pos = pos
    #to increase the execution time increase the number underneath
    if counter == 1000:
        break
print("- TIMEOUT!- ")
