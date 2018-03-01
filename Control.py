
from tkinter import *
import RPi.GPIO as GPIO
import os
import urllib.request
import urllib.parse
from time import sleep
import threading
import socket

###############################################################################
host       = "192.168.1.169"       # Ip address of server
port       = 5051                  # tcp port of server
delay      = 5                     # This is for testing purposes
pinlist    = [2,3,4,5,6,7,8,9]     # Add your relay Pins BCM
folderDir  = os.getcwd()           # get Current folder directory for Bin
###############################################################################

GPIO.setmode(GPIO.BCM)
for item in pinlist:
    GPIO.setup (item,GPIO.OUT)
    GPIO.output(item,GPIO.HIGH)

def resetButtons():
    for item in pinlist:
        print(GPIO.input(item))
        GPIO.output(item,GPIO.HIGH)
        sleep(.2)


#resetButtons()
window = Tk()
window.title("CRES AUTOMATION")
window.geometry('800x480')

#UNCOMMENT THE TWO LINES BELOW FOR FULL SCREEN MODE
#window.overrideredirect(True)
#window.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

label = Label(window, text="CRES AUTOMATION")

button1 = Button(window, text="Click Me")
button2 = Button(window, text="Click Me")
button3 = Button(window, text="Click Me")
button4 = Button(window, text="Click Me")
button5 = Button(window, text="Click Me")
button6 = Button(window, text="Click Me")
button7 = Button(window, text="Click Me")
button8 = Button(window, text="Click Me")

label.grid(column=0,row=0,columnspan=2)
button1.grid(column=0, row=1)
button2.grid(column=1, row=1)
button3.grid(column=2, row=1)
button4.grid(column=3, row=1)
button5.grid(column=0, row=2)
button6.grid(column=1, row=2)
button7.grid(column=2, row=2)
button8.grid(column=3, row=2)

b1_on  = PhotoImage(file = folderDir + '/bin/button1_on.gif')
b2_on  = PhotoImage(file = folderDir + '/bin/button2_on.gif')
b3_on  = PhotoImage(file = folderDir + '/bin/button3_on.gif')
b4_on  = PhotoImage(file = folderDir + '/bin/button4_on.gif')
b5_on  = PhotoImage(file = folderDir + '/bin/button5_on.gif')
b6_on  = PhotoImage(file = folderDir + '/bin/button6_on.gif')
b7_on  = PhotoImage(file = folderDir + '/bin/button7_on.gif')
b8_on  = PhotoImage(file = folderDir + '/bin/button8_on.gif')

b1_off = PhotoImage(file = folderDir + '/bin/button1_off.gif')
b2_off = PhotoImage(file = folderDir + '/bin/button2_off.gif')
b3_off = PhotoImage(file = folderDir + '/bin/button3_off.gif')
b4_off = PhotoImage(file = folderDir + '/bin/button4_off.gif')
b5_off = PhotoImage(file = folderDir + '/bin/button5_off.gif')
b6_off = PhotoImage(file = folderDir + '/bin/button6_off.gif')
b7_off = PhotoImage(file = folderDir + '/bin/button7_off.gif')
b8_off = PhotoImage(file = folderDir + '/bin/button8_off.gif')

def button_state_off(button):
    if(button == 1):
        button1.config(image=b1_off)
    if(button == 2):
        button2.config(image=b2_off)
    if(button == 3):
        button3.config(image=b3_off)
    if(button == 4):
        button4.config(image=b4_off)
    if(button == 5):
        button5.config(image=b5_off)
    if(button == 6):
        button6.config(image=b6_off)
    if(button == 7):
        button7.config(image=b7_off)
    if(button == 8):
        button8.config(image=b8_off)
def button_state_on(button):
    if(button == 1):
        button1.config(image=b1_on)
    if(button == 2):
        button2.config(image=b2_on)
    if(button == 3):
        button3.config(image=b3_on)
    if(button == 4):
        button4.config(image=b4_on)
    if(button == 5):
        button5.config(image=b5_on)
    if(button == 6):
        button6.config(image=b6_on)
    if(button == 7):
        button7.config(image=b7_on)
    if(button == 8):
        button8.config(image=b8_on)
#Switch the GPIO.LOW and GPIO.HIGH in the function below If On is off and off is on
def toggle(pin,button):
    if GPIO.input(pin):
        print("On")
        GPIO.output(pin,GPIO.LOW)
        button_state_on(button)
    elif(not GPIO.input(pin)):
        print("Off")
        GPIO.output(pin,GPIO.HIGH)
        button_state_off(button)
def getPin(id):
    return pinlist[id-1]

def customControlGPIO(relay, state):
    print("HERE")
    if(relay == -1 and state == -1):
        return 0
    GPIO.output(getPin(relay), state)
    print("GPIOSET")
    print(state)
    if state == 1:
        button_state_on(relay)
        print("relay on")
    elif state == 0:
        button_state_off(relay)
        print("relay Off")
def processNetworkData(data):
    relay, state = data.split(",")
    relay = int(relay)
    state = int(state)
    print("relay",relay,",","state",state)
    customControlGPIO(relay, state)
def getControl():
    while True:
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((host, port))
        except:
            print("Sever Offline")
        while True:
            try:
                data = s.recv(1024)
                data = data.decode('utf-8')
                print(data)
            except:
                data = "0"
                s.close()
                break
            if (data != "0"):
                processNetworkData(data)






window.config(background='#222a35')
label_font = ('times',20,'bold')
label.config(bg='#222a35', fg='red')
label.config(font=label_font)

button1.config(image=b1_off,height=200,width=200,command=lambda:toggle(pinlist[0],1))
button2.config(image=b2_off, height=200,width=200,command=lambda:toggle(pinlist[1],2))
button3.config(image=b3_off, height=200,width=200,command=lambda:toggle(pinlist[2],3))
button4.config(image=b4_off, height=200,width=200,command=lambda:toggle(pinlist[3],4))
button5.config(image=b5_off, height=200,width=200,command=lambda:toggle(pinlist[4],5))
button6.config(image=b6_off, height=200,width=200,command=lambda:toggle(pinlist[5],6))
button7.config(image=b7_off, height=200,width=200,command=lambda:toggle(pinlist[6],7))
button8.config(image=b8_off, height=200,width=200,command=lambda:toggle(pinlist[7],8))


if __name__ =='__main__':
    t = threading.Thread(target = getControl)
    t.daemon = True
    t.start()
    window.mainloop()
