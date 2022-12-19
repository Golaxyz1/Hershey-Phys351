import RPi.GPIO as GPIO
from time import sleep
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import math


GPIO.setmode(GPIO.BCM)
#####  Rpi Pin Assignment
'''
Servo
X_rock = 17
Y_rock = 27

Rowing Stepper
Row_A1 = 5
Row_A2 = 6
Row_B1 = 26
Row_B2 = 13

Moving Stepper
Move_A1 = 24
Move_A2 = 25
Move_B1 = 16
Move_B2 = 12

Pin 1 (3.3V) for driver motor sleep
Pin 2 (5V) for Music Power
Pin 6 (GND) for Music GND
'''
####----------------------------------------------------------------PIN SETUP-------------------------------------------------------#################
X_rock = 17
Y_rock = 27
GPIO.setup(X_rock,GPIO.OUT)  ##  Setup servo, Horizontal
GPIO.setup(Y_rock,GPIO.OUT)  ##  Setup servo, Vertical
pwm1=GPIO.PWM(X_rock,50)
pwm1.start(0)
pwm2=GPIO.PWM(Y_rock,50)
pwm2.start(0)
GPIO.setup(22,GPIO.OUT)             ### pin 22 controls the on/off of the stepper drivers
GPIO.output(22,GPIO.LOW)            ### initially set the driver to sleep mode
Row_A1 = 5
Row_A2 = 6
Row_B1 = 26
Row_B2 = 13
GPIO.setup(Row_A1,GPIO.OUT)  ##A1, Row
GPIO.setup(Row_A2,GPIO.OUT)  ##A2, Row
GPIO.setup(Row_B1,GPIO.OUT)  ##B1, Row
GPIO.setup(Row_B2,GPIO.OUT)  ##B2, Row

Move_A1 = 24
Move_A2 = 25
Move_B1 = 16
Move_B2 = 12
GPIO.setup(Move_A1,GPIO.OUT)  ##A1, Move
GPIO.setup(Move_A2,GPIO.OUT)  ##A2, Move
GPIO.setup(Move_B1,GPIO.OUT)  ##B1, Move
GPIO.setup(Move_B2,GPIO.OUT)  ##B2, Move

####----------------------------------------------------------------END OF PIN SETUP-------------------------------------------------------#################


    ###----------------------------------------------------------------ROCKING SERVOS----------------------------------------------------###
def UP_rock(position,speed = 0.8):                      ###Upper servo, controlling Vertical Rocking
    pwm1.ChangeDutyCycle(8.5+0.5*math.sin(2*speed*position))
def DOWN_rock(position,speed = 0.8):                    ###Lower servo, controlling Horizontal Rocking
    pwm2.ChangeDutyCycle(8.2+0.5*math.sin(speed*position))
def rock(position,speed = 0.8):                         ###Rock in both directions simultaneously
    UP_rock(position,speed)
    DOWN_rock(position,speed)
def rock_fast(position):    ###Change rocking speed to fast. Index is used to track the position.
    while(1):
        a = 0
        while(a <= 250):
            rock(position,speed = 1)
            position += math.pi / 125
            sleep(0.0064)
            a += 1
        root.update()       ###Related to the User Interface. See code in UI to understand.
def rock_slow(position):    ###Change rocking speed to slow. Index is used to track the position.
    while(1):
        a = 0
        while(a <= 250):
            rock(position,speed = 0.8)
            position += math.pi / 125
            sleep(0.008)
            a += 1
        root.update()
def Y_rock(position):       ###Only rock Horizontal. Index is used to track the position.
    while(1):
        a = 0
        while(a <= 250):
            DOWN_rock(position,speed = 0.8)
            position += math.pi / 125
            sleep(0.008)
            a += 1
        root.update()
def X_rock(position):       ###Only rock Vertical. Index is used to track the position.
    while(1):
        a = 0
        while(a <= 250):
            UP_rock(position,speed = 0.8)
            position += math.pi / 125
            sleep(0.008)
            a += 1
        root.update()

####------------------------------------------------------------------------------------------------Rock, Row, and Move Together-----------------------------------------------------------------------------------------####
def forward_cw(pos,fast = 0):           ###Move and Row forward while rocking
    GPIO.output(22,GPIO.HIGH)           ###Wake the drivers
    
    if fast == 0:                       ### Determine if move and rock FAST or SLOW
        speed = 0.8
        pulse = 0.001
    else:
        speed = 1
        pulse = 0.0008
    time = 0
    while(time < 4000):                 ### Move clockwise means going forward in this project.
        rock(pos,speed)                 ### Rock at the same time
        pos += math.pi / 125
        GPIO.output(Move_A1,GPIO.HIGH)
        GPIO.output(Move_B1,GPIO.HIGH)
        GPIO.output(Move_A2,GPIO.LOW)
        GPIO.output(Move_B2,GPIO.LOW)
        GPIO.output(Row_A1,GPIO.HIGH)
        GPIO.output(Row_B1,GPIO.LOW)
        GPIO.output(Row_A2,GPIO.LOW)
        GPIO.output(Row_B2,GPIO.LOW)
        time += 1
        sleep(pulse)                    #block1


        GPIO.output(Move_A1,GPIO.LOW)
        GPIO.output(Move_B1,GPIO.HIGH)
        GPIO.output(Move_A2,GPIO.HIGH)
        GPIO.output(Move_B2,GPIO.LOW)
        GPIO.output(Row_A1,GPIO.HIGH)
        GPIO.output(Row_B1,GPIO.HIGH)
        GPIO.output(Row_A2,GPIO.LOW)
        GPIO.output(Row_B2,GPIO.LOW)
        time += 1
        sleep(pulse)                    #block2

        
        GPIO.output(Move_A1,GPIO.LOW)
        GPIO.output(Move_B1,GPIO.LOW)
        GPIO.output(Move_A2,GPIO.HIGH)
        GPIO.output(Move_B2,GPIO.HIGH)
        GPIO.output(Row_A1,GPIO.LOW)
        GPIO.output(Row_B1,GPIO.HIGH)
        GPIO.output(Row_A2,GPIO.LOW)
        GPIO.output(Row_B2,GPIO.LOW)
        time += 1
        sleep(pulse)                    #block3

        
        GPIO.output(Move_A1,GPIO.HIGH)
        GPIO.output(Move_B1,GPIO.LOW)
        GPIO.output(Move_A2,GPIO.LOW)
        GPIO.output(Move_B2,GPIO.HIGH)
        GPIO.output(Row_A1,GPIO.LOW)
        GPIO.output(Row_B1,GPIO.HIGH)
        GPIO.output(Row_A2,GPIO.HIGH)
        GPIO.output(Row_B2,GPIO.LOW)
        time += 1
        sleep(pulse)                    #block4

        
        GPIO.output(Move_A1,GPIO.HIGH)
        GPIO.output(Move_B1,GPIO.HIGH)
        GPIO.output(Move_A2,GPIO.LOW)
        GPIO.output(Move_B2,GPIO.LOW)
        GPIO.output(Row_A1,GPIO.LOW)
        GPIO.output(Row_B1,GPIO.LOW)
        GPIO.output(Row_A2,GPIO.HIGH)
        GPIO.output(Row_B2,GPIO.LOW)
        time += 1
        sleep(pulse)                    #block5

        
        GPIO.output(Move_A1,GPIO.LOW)
        GPIO.output(Move_B1,GPIO.HIGH)
        GPIO.output(Move_A2,GPIO.HIGH)
        GPIO.output(Move_B2,GPIO.LOW)  
        GPIO.output(Row_A1,GPIO.LOW)
        GPIO.output(Row_B1,GPIO.LOW)
        GPIO.output(Row_A2,GPIO.HIGH)
        GPIO.output(Row_B2,GPIO.HIGH)
        time += 1
        sleep(pulse)                    #block6

        
        GPIO.output(Move_A1,GPIO.LOW)
        GPIO.output(Move_B1,GPIO.LOW)
        GPIO.output(Move_A2,GPIO.HIGH)
        GPIO.output(Move_B2,GPIO.HIGH)
        GPIO.output(Row_A1,GPIO.LOW)
        GPIO.output(Row_B1,GPIO.LOW)
        GPIO.output(Row_A2,GPIO.LOW)
        GPIO.output(Row_B2,GPIO.HIGH)
        time += 1
        sleep(pulse)                    #block7

        
        GPIO.output(Move_A1,GPIO.HIGH)
        GPIO.output(Move_B1,GPIO.LOW)
        GPIO.output(Move_A2,GPIO.LOW)
        GPIO.output(Move_B2,GPIO.HIGH)
        GPIO.output(Row_A1,GPIO.HIGH)
        GPIO.output(Row_B1,GPIO.LOW)
        GPIO.output(Row_A2,GPIO.LOW)
        GPIO.output(Row_B2,GPIO.HIGH)
        time += 1
        sleep(pulse)                    #block8
    GPIO.output(22,GPIO.LOW)            ###Set driver to sleep
    while(1):                           ### Continue rocking when the moving motion ends and enable the user to continue using the interface.
        a = 0
        while(a <= 250):
            rock(pos,speed)
            pos += math.pi / 125
            a += 1
            sleep(8*pulse)
        enable_button()
        root.update()

def backward_ccw(pos,fast = 0):         ###Move and Row backward while rocking
    GPIO.output(22,GPIO.HIGH)           ###Wake the drivers
    time = 0                            ### Determine if move and rock FAST or SLOW
    if fast == 0:
        speed = 0.8
        pulse = 0.001
    else:
        speed = 1
        pulse = 0.0008
    while(time < 4000):                 ### Move counterclockwise means going backward in this project.
        rock(pos,speed)                 ### Rock at the same time
        pos += math.pi / 125
        GPIO.output(Move_A1,GPIO.HIGH)
        GPIO.output(Move_B1,GPIO.LOW)
        GPIO.output(Move_A2,GPIO.LOW)
        GPIO.output(Move_B2,GPIO.HIGH)
        GPIO.output(Row_A1,GPIO.HIGH)
        GPIO.output(Row_B1,GPIO.LOW)
        GPIO.output(Row_A2,GPIO.LOW)
        GPIO.output(Row_B2,GPIO.HIGH)
        time += 1
        sleep(pulse)                    #block8

        
        GPIO.output(Move_A1,GPIO.LOW)
        GPIO.output(Move_B1,GPIO.LOW)
        GPIO.output(Move_A2,GPIO.HIGH)
        GPIO.output(Move_B2,GPIO.HIGH)
        GPIO.output(Row_A1,GPIO.LOW)
        GPIO.output(Row_B1,GPIO.LOW)
        GPIO.output(Row_A2,GPIO.LOW)
        GPIO.output(Row_B2,GPIO.HIGH)
        time += 1
        sleep(pulse)                    #block7

        
        GPIO.output(Move_A1,GPIO.LOW)
        GPIO.output(Move_B1,GPIO.HIGH)
        GPIO.output(Move_A2,GPIO.HIGH)
        GPIO.output(Move_B2,GPIO.LOW)
        GPIO.output(Row_A1,GPIO.LOW)
        GPIO.output(Row_B1,GPIO.LOW)
        GPIO.output(Row_A2,GPIO.HIGH)
        GPIO.output(Row_B2,GPIO.HIGH)
        time += 1
        sleep(pulse)                    #block6

        
        GPIO.output(Move_A1,GPIO.HIGH)
        GPIO.output(Move_B1,GPIO.HIGH)
        GPIO.output(Move_A2,GPIO.LOW)
        GPIO.output(Move_B2,GPIO.LOW)
        GPIO.output(Row_A1,GPIO.LOW)
        GPIO.output(Row_B1,GPIO.LOW)
        GPIO.output(Row_A2,GPIO.HIGH)
        GPIO.output(Row_B2,GPIO.LOW)
        time += 1
        sleep(pulse)                    #block5

        
        GPIO.output(Move_A1,GPIO.HIGH)
        GPIO.output(Move_B1,GPIO.LOW)
        GPIO.output(Move_A2,GPIO.LOW)
        GPIO.output(Move_B2,GPIO.HIGH)
        GPIO.output(Row_A1,GPIO.LOW)
        GPIO.output(Row_B1,GPIO.HIGH)
        GPIO.output(Row_A2,GPIO.HIGH)
        GPIO.output(Row_B2,GPIO.LOW)
        time += 1
        sleep(pulse)                    #block4

        
        GPIO.output(Move_A1,GPIO.LOW)
        GPIO.output(Move_B1,GPIO.LOW)
        GPIO.output(Move_A2,GPIO.HIGH)
        GPIO.output(Move_B2,GPIO.HIGH)
        GPIO.output(Row_A1,GPIO.LOW)
        GPIO.output(Row_B1,GPIO.HIGH)
        GPIO.output(Row_A2,GPIO.LOW)
        GPIO.output(Row_B2,GPIO.LOW)
        time += 1
        sleep(pulse)                    #block3

        
        GPIO.output(Move_A1,GPIO.LOW)
        GPIO.output(Move_B1,GPIO.HIGH)
        GPIO.output(Move_A2,GPIO.HIGH)
        GPIO.output(Move_B2,GPIO.LOW)
        GPIO.output(Row_A1,GPIO.HIGH)
        GPIO.output(Row_B1,GPIO.HIGH)
        GPIO.output(Row_A2,GPIO.LOW)
        GPIO.output(Row_B2,GPIO.LOW)
        time += 1
        sleep(pulse)                    #block2

        
        GPIO.output(Move_A1,GPIO.HIGH)
        GPIO.output(Move_B1,GPIO.HIGH)
        GPIO.output(Move_A2,GPIO.LOW)
        GPIO.output(Move_B2,GPIO.LOW)
        GPIO.output(Row_A1,GPIO.HIGH)
        GPIO.output(Row_B1,GPIO.LOW)
        GPIO.output(Row_A2,GPIO.LOW)
        GPIO.output(Row_B2,GPIO.LOW)
        time += 1
        sleep(pulse)                    #block1
    GPIO.output(22,GPIO.LOW)            ###Set driver to sleep
    while(1):                           ### Continue rocking when the moving motion ends and enable the user to continue using the interface.
        a = 0
        while(a <= 250):
            rock(pos,speed)
            pos += math.pi / 125
            a += 1
            sleep(8*pulse)
        enable_button()
        root.update()
def stop_everything():                  ###reposition servos to the middle and stop everything and cleanup pins. Executed after Stop button is clicked by user. End of the sail. 
    GPIO.output(Move_A1,GPIO.LOW)
    GPIO.output(Move_B1,GPIO.LOW)
    GPIO.output(Move_A2,GPIO.LOW)
    GPIO.output(Move_B2,GPIO.LOW)
    GPIO.output(Row_A1,GPIO.LOW)
    GPIO.output(Row_B1,GPIO.LOW)
    GPIO.output(Row_A2,GPIO.LOW)
    GPIO.output(Row_B2,GPIO.LOW)
    GPIO.output(22,GPIO.LOW)
    pwm1.ChangeDutyCycle(8.5)
    pwm2.ChangeDutyCycle(8.2)
    sleep(1)
    GPIO.output(17,GPIO.LOW)
    GPIO.output(27,GPIO.LOW)
    sleep(1)                                            ###need enough time for the voltage to stablize. Otherwise the servos receive false signal.
    GPIO.cleanup()
    sleep(1)

####--------------------------------------------------------------------------------------- --END OF ALL ROCKING, ROWING, AND MOVING-------------------------------------------------------------------------------####



####--------------------------------------------------------------------------------------- --BEGIN OF UI-------------------------------------------------------------------------------####
root = tk.Tk() #root is the name of the main window
root.title('The Rise of Grogu')

#Window Size
window_width = 500
window_height = 400

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the pop up window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

#Change corner icon with a .ico file
#root.iconbitmap(file_location)

#Making the grid 3x3 for placing features
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)


    ###-------------------------------------------------------------------Disable/Enable button when one is pushed---------------------------------------------------------------###
def disable_button():
    Rock_slower.state(['disabled'])
    Rock_faster.state(['disabled'])
    Slowfwd.state(['disabled'])
    Fastfwd.state(['disabled'])
    Fastback.state(['disabled'])
    Slowback.state(['disabled'])
    H_rock.state(['disabled'])
    V_rock.state(['disabled'])
    Stop.state(['disabled'])
def enable_button():
    Rock_slower.state(['!disabled'])
    Rock_faster.state(['!disabled'])
    Slowfwd.state(['!disabled'])
    Fastfwd.state(['!disabled'])
    Fastback.state(['!disabled'])
    Slowback.state(['!disabled'])
    H_rock.state(['!disabled'])
    V_rock.state(['!disabled'])
    Stop.state(['!disabled'])
###------------------------------------------------------------------- END OF Disable/Enable button when one is pushed---------------------------------------------------------------###

###-------------------------------------------------------------- functions that are called when buttons are pushed-----------------------------------------------------------------###
def forward_slow():
    disable_button()
    root.update()
    forward_cw(position,0)

def forward_fast():
    disable_button()
    root.update()
    forward_cw(position,1)

def back_fast():
    disable_button()
    root.update()
    backward_ccw(position,1)
    
def back_slow():
    disable_button()
    root.update()
    backward_ccw(position,0)
    
def stop():
    stop_everything()
    
def rock_faster():
    rock_fast(position)
    
def rock_slower():
    rock_slow(position)
    
def H_rock():
    Y_rock(position)
    
def V_rock():
    X_rock(position)
    
ipading = {'ipadx' : 7, 'ipady': 7}

message = tk.Label(root, text= "To set sail press one of the buttons below")
message.grid(column = 0, row = 0, columnspan = 2, ipady = 50)
 #command = function, allows you to choose a function to call when button is pushed
Rock_slower = ttk.Button(text= ' < Rock Slow', command = rock_slower)
Rock_slower.grid(column = 1, row = 2, **ipading)

Rock_faster = ttk.Button(text= ' < Rock Fast', command = rock_faster)
Rock_faster.grid(column = 0, row = 2, **ipading)

Slowfwd = ttk.Button(text= 'Slow Forward > ', command = forward_slow)
       
Slowfwd.grid(column = 1, row = 3, **ipading)

Fastfwd = ttk.Button(text= ' < Fast Forward', command = forward_fast)
Fastfwd.grid(column = 0, row = 3, **ipading)

Slowback = ttk.Button(text= ' < Slow Back', command = back_slow)
Slowback.grid(column = 1, row = 4, **ipading)

Fastback = ttk.Button(text= ' < Fast Back', command = back_fast)
Fastback.grid(column = 0, row = 4, **ipading)

H_rock = ttk.Button(text= ' Horizontal Rock', command = H_rock)
H_rock.grid(column = 1, row = 5, **ipading)

V_rock = ttk.Button(text= ' Vertical Rock', command = V_rock)
V_rock.grid(column = 0, row = 5, **ipading)

Stop = ttk.Button(text= ' < Stop', command = stop)
Stop.grid(column = 1, row = 6, **ipading)

###------------------------------------------------------------------------------------------------END OF UI SETUP-----------------------------------------------------------------------------------###try:


###---------------------------------------------------------------------------------MAIN PROGRAM THAT RUNS WHEN THE PROGRAM STARTS----------------------------------------------------------------###
position = 0
sleep(0.1)
pwm1.ChangeDutyCycle(8.5)
pwm2.ChangeDutyCycle(8.2)
sleep(0.5)
while(1):           ### Rock in both directions slowly as a default 
    rock(position)
    position += math.pi / 125
    sleep(0.008)
    root.update()


