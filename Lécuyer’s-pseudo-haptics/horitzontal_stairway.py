# AUTHOR: JAUME BENSENY
#
# IMPORTANT : EXECUTION TIME IS CONTROLLER BY COUNTER WITHIN THE WHILE LOOP
import subprocess
from math import fabs
import re
import numpy
from subprocess import check_output

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
def predict(pos,last_pos,x_lenght):
    dif = pos[0] - last_pos
    threshold = pos[0] // 100
    #if movement doesnt reach minium threshold cursor is sent back
    if fabs(dif) < threshold:
        print("SENT BACK!->",pos[0],threshold,dif)
        return last_pos
    else:
        return pos[0]

#generate map
x_lenght = 800
y_lenght = 600
imap = numpy.zeros((x_lenght,y_lenght))
#we create an steep slope from left to right
for i in range(x_lenght):
    for j in range(y_lenght):
        imap[i][j]= j
#variables
counter = 0
pos = []
#initial position
pointer_moveto("0","300")
last_pos = 0
#pos =  numpy.zeros(max_counter)
print("*** HELLO *** ")
print("- Try to move the mouse to your right and jump the different levels ")
while True:
    pos = pointer_location()
    #print("TEMP POS ->", pos[0], pos[1])
    a = predict(pos,last_pos,x_lenght)
    pointer_moveto(str(a),str(pos[1]))
    counter = counter + 1
    last_pos = pos[0]
    if counter == 1000:
        break
    
print("FINAL END, COUNTER ->", counter)


