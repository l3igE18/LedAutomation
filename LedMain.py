#from threading import Thread
import board
import neopixel
import time
import sys
import random
import math
import RPi.GPIO as GPIO
#thread_running = True
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)#,initial=GPIO.HIGH)
#GPIO.setup(18, GPIO.OUT)
pixels = neopixel.NeoPixel(board.D18, 960, brightness=1.0, auto_write=False)
# below are support functions that are used by all functions


def colours(colour):

    return{
        'red': [255, 0, 0],
        'blue': [0, 0, 255],
        'better_blue':[0,0,50],
        'green': [0, 255, 0],
        'yellow': [255, 255, 0],
        'orange': [255, 127, 0],
        'purple': [128, 0, 128],
        'violet': [143, 0, 255],
        'white': [255, 255, 255],
        'better_white':[65,65,65],
        'black': [0, 0, 0],
        'rainbow': [[255, 0, 0], [0, 0, 255], [0, 255, 0]]
    }.get(colour, -1)


def colourCheck(argument, colour1, colour2, steps):

    if argument == 0:
        if (colour1 > colour2):
            if colour1+(steps * -1) <= colour2:
                return colour2
            return colour1 + (-1 * steps)
        if colour1 == colour2:
            return colour1
        else:
            if colour1+(steps * 1) >= colour2:
                return colour2
            return colour1 + (1 * steps)
    if argument == 1:
        if colour1 >= colour2:
            return -1
        if colour1 <= colour2:
            return 1

    return 0
# below are the functions that control that leds


def off():
    pixels.deinit()

def powerDown():
    GPIO.output(17, GPIO.HIGH)
    GPIO.cleanup()


def on():
    pixels = neopixel.NeoPixel(board.D18, 960, brightness=1.0, auto_write=False)
    GPIO.output(17, GPIO.LOW)


def singlepixel(sColour, pixel):
    pixels[pixel] = sColour
    pixels.show()


def fill(sColour,brightness):
    colourShow=[0,0,0]
    try:
        if not sColour[0].isdigit():
            colourORG=colours(sColour)
            colourShow[0]=colourORG[0]*float(brightness)
            colourShow[1]=colourORG[1]*float(brightness)
            colourShow[2]=colourORG[2]*float(brightness)
            pixels.fill(colourShow)
            pixels.show()
        else:
            lColour = list(map(int, sColour.split(",")))
            colourShow[0]=lColour[0]*float(brightness)
            colourShow[1]=lColour[1]*float(brightness)
            colourShow[2]=lColour[2]*float(brightness)
            pixels.fill(colourShow)
            pixels.show()
    except ValueError:
        print("invaild colour")


def presets(preset, colourSel):

    if preset == 'door':
        i = 646
        for i in range(646, 778):
            pixels[i] = colourSel
        pixels.show()


def blink(colourSel, hold=0.25, cycles=1, seperator=0):
    c = 0
    for i in range(0, cycles):
        if(seperator == 0):
            while c != len(colourSel):
                pixels.fill(colourSel[c])
                pixels.show()
                time.sleep(hold)
                pixels.fill((0, 0, 0))
                pixels.show()
                time.sleep(hold)
                c = c+1
            c = 0
        elif(seperator == 1):
            while c != len(colourSel):
                pixels.fill(colourSel[c])
                pixels.show()
                time.sleep(hold)
                c = c+1
            c = 0

def breath(colourSel,speed,duration=-1):

    pixels.brightness=0.25
    pixels.show


def comet(colourSel, trail, cycles, start=1, end=960):
    c = 0
    loop = 0
    pixels[0] = colourSel[c] 
    while True:

        for i in range(start-1, end):
            pixels2 = pixels[:]
            for j in range(start, end):
                pixels[j] = pixels2[j-1]
            pixels.show()
            if i == trail:
                c = 1
                pixels[0] = colourSel[c]

            i = i+1
        loop = loop+1
        if loop == cycles:
            print("cycles "+str(int(loop))+"/"+str(cycles)+" completed")
            return None
        else:
            c = 0
            pixels[0] = colourSel[c]
            print("cycles "+str(int(loop))+"/"+str(cycles)+" completed")


def bounce(colourSel, trail, cycles, start=1, end=960):
    c = 0
    loop = 0
    pixels[0] = colourSel[c]
    while True:

        for i in range(start-1, end):
            pixels2 = pixels[:]
            for j in range(start, end):
                pixels[j] = pixels2[j-1]
            pixels.show()
            if i == trail:
                c = 1
                pixels[0] = colourSel[c]
            i = i+1
        for i in range(end, start):
            pixels2 = pixels[:]
            for j in range(end-1, start):
                pixels[j] = pixels2[j+1]
            pixels.show()
            i = i-1

        loop = loop+1
        if loop == cycles:
            print("cycles "+str(int(loop))+"/"+str(cycles)+" completed")
            return None
        else:
            c = 0
            pixels[0] = colourSel[c]
            print("cycles "+str(int(loop))+"/"+str(cycles)+" completed")


def chase(colourSel, gap, steps, cycles, start=1, end=960):
    c = 0
    loop = 0
    while True:

        pixels[0] = colourSel[c]
        for i in range(start-1, gap):
            pixels2 = pixels[:]
            for j in range(start, end):
                pixels[j] = pixels2[j-1]
            pixels.show()

            i = i+(1*steps)
            loop = loop+1
            if loop/end == cycles:
                print("cycles "+str(int(loop/end)) +
                      "/"+str(cycles)+" completed")
                return None
            elif (loop/end).is_integer():
                print("cycles "+str(int(loop/end)) +
                      "/"+str(cycles)+" completed")
        c = c+1

        if c == len(colourSel):
            c = 0


def fade(colourSel, hold, steps, start=0, end=960):
    color = [0, 0, 0]
    c = 0
    while True:
        if color[0] == colourSel[c][0] and color[1] == colourSel[c][1] and color[2] == colourSel[c][2]:

            if c >= len(colourSel)-1:
                c = 0
            else:
                c = c+1
            time.sleep(hold)
        color[0] = colourCheck(0, color[0], colourSel[c][0], steps)
        color[1] = colourCheck(0, color[1], colourSel[c][1], steps)
        color[2] = colourCheck(0, color[2], colourSel[c][2], steps)
        pixels.fill(color)
        pixels.show()

def christmasLights():
    CHcolours=("blue","red") #,"green","purple","yellow","orange")
    j=0
    for k in range (1,8):

        for i in range (0,959):
        
            if (i%15==0):
                pixels.show()
                if j<(len(CHcolours)-1):
                    j=j+1
                else:j=0
            pixels[i]=colours(CHcolours[j])
            
        j=j+1

def test():
    for i in range(0,959):
        pixels[i]=(22,22,22)
    pixels.show()
def brightness(brightnessValue):
    
    pixels.brightness=0.1
def test2():
    
    print(pixels.property)


# main loop that runs the function slection routine


def main():
    while True:

        try:
        
            x = input("Please select function to run:\n").strip()

            if x == 'help':
                print(
                    "\nCommands:\noff\ncolour\nfade\nchase(to come)\nrainbow fade\nrainbow chase\nexit\n")
            elif x == 'off':
                off()
            elif x == 'power down':
                powerDown()
            elif x == 'on':
                on()
            elif x == 'rainbow fade':
                fade([colours("red"), colours("orange"), colours("yellow"), colours(
                    "green"), colours("blue"), colours("purple"), colours("violet")], 0, 1)
            elif x == 'blink':
                x = input(
                    "Please enter a list of colours:\n(seperate colours by a space)\n").strip()
                xcolour = list(map(colours, x.split(" ")))
                y = input("What hold time do you want?\n").strip()
                z = input("how many cycles?\n").strip()
                blink(xcolour, float(y), int(z))
            elif x == 'fill':
                x = input("Please enter a colour:\n")
                y= input("Please enter the brightness\n")
                fill(x,y)
            elif x == 'rainbow chase':
                y = input("Please enter gap amount\n(in pixels)\n").strip()
                z = input("at what speed?\n").strip()
                h = input("Please enter number of cycles\n").strip()
                chase([colours("red"), colours("orange"), colours("yellow"), colours("green"), colours(
                    "blue"), colours("purple"), colours("violet")], int(y), int(z), int(h))
            elif x == 'fade':
                x = input(
                    "Please enter a list of colours:\n(seperate colours by a space)\n").strip()
                xcolour = list(map(colours, x.split(" ")))
                y = input("What hold time do you want?\n").strip()
                z = input("at what speed?\n").strip()
                fade(xcolour, int(y), int(z))
            elif x == 'chase':
                x = input(
                    "Please enter a list of colours:\n(seperate colours by a space)\n").strip()
                xcolour = list(map(colours, x.split(" ")))
                y = input("Please enter gap amount\n(in pixels)\n").strip()
                z = input("at what speed?\n").strip()
                h = input("Please enter number of cycles\n").strip()
                chase(xcolour, int(y), int(z), int(h))
            elif x == 'random rainbow':
                print("in the works")
            elif x == 'rainbow blink':

                y = input("What hold time do you want?\n").strip()
                h = input("Please enter number of cycles\n").strip()
                blink([colours("red"), colours("orange"), colours("yellow"), colours("green"), colours(
                    "blue"), colours("purple"), colours("violet")], float(y), int(h), 1)

            elif x == 'exit':
                off()
                try:
                    GPIO.cleanup()
                    sys.exit()
                except:
                    sys.exit()
                
            elif x == 'single':
                x = input("Please enter a colour\n").strip()
                xcolour = colours(x)
                y = input("please enter pixel address\n").strip()
                singlepixel(xcolour, int(y))
            elif x == 'preset':
                y = input("please enter preset\n").strip()
                x = input("Please enter a colour\n").strip()
                xcolour = colours(x)
                presets(y, xcolour)
            elif x == 'comet':
                x = input(
                    "Please enter a list of 2 colours:\n(seperate colours by a space)\n").strip()
                xcolour = list(map(colours, x.split(" ")))
                y = input("Please enter trail length\n(in pixels)\n").strip()
                z = input("Please enter number of cycles\n").strip()
                comet(xcolour, int(y), int(z))
            elif x == 'bounce':
                x = input(
                    "Please enter a list of 2 colours:\n(seperate colours by a space)\n").strip()
                xcolour = list(map(colours, x.split(" ")))
                y = input("Please enter trail length\n(in pixels)\n").strip()
                z = input("Please enter number of cycles\n").strip()
                bounce(xcolour, int(y), int(z))
            elif x == 'christmas lights':
                christmasLights()
            elif x=='test':
                test()
            elif x=='breath':
                x = input(
                    "Please enter a colour:\n").strip()
                xcolour = list(map(colours, x.split(" ")))
                breath(xcolour,5)
            elif x=="brightness":
                x=input("Please enter the brightness:\n").strip()
                
                brightness(x)
            elif x=="test2":
                test2()
            else:
                print("invaild try again")
        except KeyboardInterrupt:
            GPIO.cleanup()
            exit()


if __name__ == '__main__':
    main()

