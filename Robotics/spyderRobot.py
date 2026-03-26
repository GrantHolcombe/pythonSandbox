from usys import stdin  # keyboard
from uselect import poll
import time
import uasyncio as asyncio
from machine import Pin, PWM

keyboard = poll()
keyboard.register(stdin)


ROTATE_0 = 1700 #Rotate to 0° position
ROTATE_45 = 3300 #Rotate to 45° position
ROTATE_90 = 4940 #Rotate to 90° position
# ROTATE_135 = 6600 #Rotate to 135° position
ROTATE_135 = 6600 #Rotate to 135° position
ROTATE_180 = 8250 #Rotate to 180° position

# Construct PWM object, with LED on Pin(25).
for x in range(0,16,4):
    print('Leg Set:' + str(x))
    for j in range(x,x+4,1):
        globals()[f'S{j}'] = PWM(Pin(j))    
        # Set the PWM frequency.
        globals()[f'S{j}'].freq(50) # 20ms
    # duty_u16 max 65535
    #tip
#     globals()[f'S{x}'].duty_u16(ROTATE_90)
#     time.sleep(.75)
#     globals()[f'S{x}'].duty_u16(ROTATE_45 - 1000)
#     time.sleep(.05)
#     #elbow
#     globals()[f'S{x+1}'].duty_u16(ROTATE_90)
#     time.sleep(.75)
#     globals()[f'S{x+1}'].duty_u16(ROTATE_135)
#     time.sleep(.75)
#     #shoulder
#     globals()[f'S{x+2}'].duty_u16(ROTATE_90)
#     time.sleep(.75)
#     if x+2 == 6 or x+2 == 14:
#         globals()[f'S{x+2}'].duty_u16(ROTATE_135)
#         time.sleep(.75)
#     else:
#         globals()[f'S{x+2}'].duty_u16(ROTATE_45)
#         time.sleep(.75)


def step_f(legId):
    #elbow up
    globals()[f'S{legId+1}'].duty_u16(ROTATE_90 + 1100)
    time.sleep(.5)
    #front/back symetry
    if legId == 4:
        tip_stretch(12)
        #shoulder forward
        globals()[f'S{legId+2}'].duty_u16(ROTATE_180 - 200)
        time.sleep(.75)
        tip_reset(12)
    elif legId == 8:
        tip_stretch(0)
        #shoulder forward
        globals()[f'S{legId+2}'].duty_u16(ROTATE_0 + 200)
        time.sleep(.75)
    else:
        #shoulder forward
        globals()[f'S{legId+2}'].duty_u16(ROTATE_90)
        time.sleep(.5)     
    #elbow down firm
    globals()[f'S{legId+1}'].duty_u16(ROTATE_135 + 900)
    time.sleep(.5)
    if legId == 0 or legId == 8:
        #shoulder back
        globals()[f'S{legId+2}'].duty_u16(ROTATE_45 + 600)
        time.sleep(.5)
        if legId == 8:
            tip_reset(0)
    else:
        #shoulder back
        globals()[f'S{legId+2}'].duty_u16(ROTATE_135 - 600)
        time.sleep(.5)
        if legId == 4:
            tip_reset(12)
    #elbow down rest
    globals()[f'S{legId+1}'].duty_u16(ROTATE_135)
    time.sleep(.5)    
        

# single step full forward
def forward():
    step_f(0)
    step_f(12)
    step_f(4)
    step_f(8)

#turn right
def turn_right():
    step_f(12)
    step_f(8)
    
#turn left
def turn_left():
    step_f(0)
    step_f(4)
#home for servo orientation
def home():
    for x in range(16):
        globals()[f'S{x}'].duty_u16(ROTATE_90)
        time.sleep(.5)
# home()

def tips_down():
    for x in range(0,16,4):
        globals()[f'S{x}'].duty_u16(ROTATE_45 - 1000)
        time.sleep(.5)
# tips_down()

def tip_stretch(legId):
    globals()[f'S{legId}'].duty_u16(ROTATE_45)
    time.sleep(.75)
    
def tip_reset(legId):
    globals()[f'S{legId}'].duty_u16(ROTATE_45 - 1000)
    time.sleep(.1)
    globals()[f'S{legId+1}'].duty_u16(ROTATE_135)
    time.sleep(.1) 
        
while True:  # making a loop
    if keyboard.poll(0):
        char = stdin.read(1)
        print("Key: ", char)
        if char == "w":
            forward()
        if char == "a":
            turn_left()
        if char == "d":
            turn_right()
        if char == "h":
            home()
        if char == "t":
            tips_down()
                
# for x in range(15):
#     turn_left()
# for x in range(5):
#     forward()


# for x in range(3):
#     print("time: ", x+1)
#     for i in range(1700,3300,10):  
#       S2.duty_u16(i)
#       time.sleep(0.04)
#     time.sleep(0.1)
#     for i in range(3300,1700,-10):
#       S.duty_u16(i)
#       time.sleep(0.04)
#     time.sleep(0.1)
print("PWM down")
for x in range(0,16,4):
    globals()[f'S{x}'].duty_u16(0)