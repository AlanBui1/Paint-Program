#Chess Paint Project
#Alan Bui

'''

This program is a chess-themed program based on MS Paint and supports the following functions:

- Pencil
- Eraser
- Brush
- Spray Paint
- Clear Screen
- Fill Screen
- Shapes (Line, Rect, Ellipse)
- Stamps
- Backgrounds
- Change Color
- Change Weight
- Save/Load

In addition, there is a help feature which you can activate by clicking the question mark.
'''

from pygame import *
from random import *
from tkinter import *
from tkinter import filedialog
font.init()
root=Tk()
root.withdraw()

def inRect(mouseX, mouseY, x1, y1, x2, y2): #function which returns a boolean if (mouseX, mouseY) is in the rectangle with top-left corner (x1,y1) and bottom right corner (x2, y2)
    return x1 <= mouseX <= x2 and y1 <= mouseY <= y2

def inCircle(mouseX, mouseY, x, y, r): #function which returns a boolean if (mouseX, mouseY) is in the circle centered at (x, y) with radius r
    return ((mouseX-x)**2 + (mouseY-y)**2)**0.5 < r

def drawRectangle(RECT, size):

    x1 = RECT[0] #left coordinate
    y1 = RECT[1] #top coordinate
    x2 = RECT[0]+RECT[2] #right coordinate
    y2 = RECT[1]+RECT[3] #bottom coordinate
    sizeX = min(size, x2-x1) #makes sure the thickness doesn't exceed the width of the rectangle
    sizeY = min(size, y2-y1) #makes sure the thickness doesn't exceed the height of the rectangle

    draw.rect(screen, curColor, (x1, y1, x2-x1, sizeY)) #draws 4 separate rectangles as a "frame"
    draw.rect(screen, curColor, (x1, y2-sizeY, x2-x1, sizeY))
    draw.rect(screen, curColor, (x1, y1, sizeX, y2-y1))
    draw.rect(screen, curColor, (x2-sizeX, y1, sizeX, y2-y1))

    if shapeFill: #fills the rectangle if it needs to be filled
        draw.rect(screen, curColor, RECT)
    
def drawEllipse(RECT): #function to draw a filled/unfilled ellipse
    draw.ellipse(screen, curColor, (RECT[0], RECT[1], RECT[2], RECT[3]), sz)
    if shapeFill:
        draw.ellipse(screen, curColor, RECT)

def loadImage(filename, w, h): #function to return an image given the filename with width w and height h
    img = image.load("Paint-Project-Images/"+filename)
    img = transform.scale(img, (w, h))
    return img

def blitText(fontType, string, x, y, color): #function to blit a string on the screen at (x, y) given the color and font type
    txtPic = fontType.render(string, 1, color)
    screen.blit(txtPic, (x, y))

#Declare constant colors
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)

#Declare all fonts
colorFont = font.SysFont("Algerian", 10)
sizeFont = font.SysFont("COMIC SANS MS", 40)
selectFont = font.SysFont("COMIC SANS MS", 20)
infoFont = font.SysFont("Times New Roman", 20)

#set the width and height
width,height= 1200,700
screen=display.set_mode((width,height))

#the current RGB values
curR, curG, curB = "0","0","0"

#Using a chess board as a background
board = loadImage("chessboard.png", 400,400)
for i in range(400, 801, 400):
    screen.blit(board, (i, 0))
    screen.blit(board, (i, 600))
    screen.blit(board, (0, i-400))

#Loading the frame of the canvas
frame = loadImage("frame.png", 1150,500)
screen.blit(frame, (90,100))
#Defining canvasRect and drawing a White rectangle for the canvas (canvas default starts as white)
canvasRect = Rect(150,150,1000,400)
draw.rect(screen, WHITE, canvasRect)

#Loading and scaling the speech bubbles for the help feature

bubble1 = loadImage("bubble1.png", 300,200)
bubble2 = loadImage("bubble2.png", 300,200)
bubble3 = loadImage("bubble3.png", 300,200)
bubble4 = loadImage("bubble4.png", 300,200)
bubble5 = loadImage("bubble5.png", 300,200)

#Loading and scaling the question mark image
qmark = image.load("Paint-Project-Images/qmark.png")
qmark = transform.scale(qmark, (100,80))

#DEFINE ALL BACKGROUNDS
# _s is for the thumbnail for each of the backgrounds
# _f is what will be blitted to the canvas when a background is selected

##bg1 = image.load("Paint-Project-Images/bg1.png")
bg1_s = loadImage("bg1_s.png", 100,100)
bg1_f = loadImage("bg1.png", 1000,400)

bg2_s = loadImage("bg2_s.png", 100,100)
bg2_f = loadImage("bg2.png", 1000,400)

bg3_s = loadImage("bg3_s.png", 100,100)
bg3_f = loadImage("bg3.png", 1000,400)

screen.blit(bg1_s, (500,600))
screen.blit(bg2_s, (600,600))
screen.blit(bg3_s, (700,600))

#Loading and scaling the title
title = image.load("Paint-Project-Images/Title.png")
title = transform.scale(title, (title.get_width()*1//2, title.get_height()*1//2))
screen.blit(title, (width//2-title.get_width()//2-40,-10))

#DEFINE STAMPS
pawnW = loadImage("pawnW.png", 80*63//108,80)
knightW = loadImage("knightW.png", 100*68//161,100)
bishopW = loadImage("bishopW.png", 100*66//169,100)
rookW = loadImage("rookW.png", 80*73//142,80)
queenW = loadImage("queenW.png", 100*77//184,100)
kingW = loadImage("kingW.png", 100*76//214,100)

pawnB = loadImage("pawnB.png", 80*63//108,80)
knightB = loadImage("knightB.png", 100*68//161,100)
bishopB = loadImage("bishopB.png", 100*66//169,100)
rookB = loadImage("rookB.png", 80*73//142,80)
queenB = loadImage("queenB.png", 100*77//184,100)
kingB = loadImage("kingB.png", 100*76//214,100)

#list of all the images of stamps
stamps = [pawnW, knightW, bishopW, rookW, queenW, kingW, pawnB, knightB, bishopB, rookB, queenB, kingB]

#DEFINE ALL ICONS
pencilIcon = loadImage("pencilIcon.png", 80,80)
eraserIcon = loadImage("eraserIcon.png", 80,80)
brushIcon = loadImage("brushIcon.png", 80,80)
sprayIcon = loadImage("sprayIcon.png", 100,100)
bucketIcon = loadImage("bucket.png", 80,90)
XIcon = loadImage("X.png", 80,80)
saveIcon = loadImage("saveIcon.png", 50,50)
loadIcon = loadImage("loadIcon.png", 50,50)
rightArrowIcon = loadImage("rightArrow.png", 40,50)
leftArrowIcon = loadImage("leftArrow.png", 40,50)

#DEFINE ALL RECTS
weightRect = Rect(1075,25,50,50)
upArrowRect = Rect(1130,25,10,25)
downArrowRect = Rect(1130,51,10,25)
pencilRect = Rect(10,110, 80,80)
eraserRect = Rect(10,210, 80,80)
brushRect = Rect(10,310, 80,80)
sprayRect = Rect(10,410,80,80)
lineRect = Rect(210, 610, 80,80)
rectRect = Rect(310, 610, 80,80)
ellipseRect = Rect(410, 610, 80,80)
stampRect1 = Rect(800,600,100,100)
stampRect2 = Rect(900,600,100,100)
stampRect3 = Rect(1000,600,100,100)
bgRect1 = Rect(500,600,100,100)
bgRect2 = Rect(600,600,100,100)
bgRect3 = Rect(700,600,100,100)
rightArrowBox = Rect(1105,605,40,40)
leftArrowBox = Rect(1105,655,40,40)
helpRect = Rect(1150,600,50,100)
bucketRect = Rect(210, 10,80,80)
clearRect = Rect(110, 10,80,80)
saveRect = Rect(0,0,50,50)
loadRect = Rect(50,50,50,50)
fillSwitch = Rect(100,650,100,50)

selectRect = [False for i in range(21)] #list for if a tool is being selected
hoverRect = [False for i in range(21)] #list for if a tool is being hovered over
#list of all the Rects
allRects = [pencilRect, eraserRect, brushRect, sprayRect, lineRect, rectRect, ellipseRect, stampRect1, stampRect2, stampRect3, helpRect, bucketRect, clearRect, saveRect, loadRect, bgRect1, bgRect2, bgRect3 ,weightRect, upArrowRect, downArrowRect]
#list of the names of the tools
tools = ["pencil", "eraser", "brush", "spray", "line", "rect", "ellipse", "stamp1", "stamp2", "stamp3", "help"]

#DRAWING ALL ICONS

screen.blit(pencilIcon, (pencilRect[0],pencilRect[1]))
screen.blit(eraserIcon, (eraserRect[0], eraserRect[1]))
screen.blit(brushIcon, (brushRect[0], brushRect[1]))
screen.blit(sprayIcon, (sprayRect[0],sprayRect[1]-10))
screen.blit(bucketIcon, (bucketRect[0], bucketRect[1]))
screen.blit(XIcon, (clearRect[0], clearRect[1]))
screen.blit(saveIcon, (saveRect[0], saveRect[1]))
screen.blit(loadIcon, (loadRect[0], loadRect[1]))
draw.line(screen, BLACK, (285,615) ,(215,685), 3)
draw.rect(screen, BLACK, (320,620, 60,60), 2)
draw.ellipse(screen, BLACK, (420,620,60,60), 2)

draw.rect(screen, RED, fillSwitch)
blitText(sizeFont, "OFF", fillSwitch[0]+10, fillSwitch[1], BLACK)
blitText(sizeFont, "FILL:", fillSwitch[0], fillSwitch[1]-50, BLACK)

curCursor = 0 #the current cursor
#defining the possible cursors
pencilcursor = loadImage("pencilcursor.png", 40,40)
handcursor = SYSTEM_CURSOR_HAND
brushcursor = loadImage("brushcursor.png", 30,30)

#list of the cursors
cursorList = [handcursor, pencilcursor, brushcursor]

#setting all defaults
running=True
drawing = False #boolean for if something is trying to be drawn
typingFont = False #boolean for if the user is trying to change the weight using keyboard
sz = 1 #default weight of tools is 1
stampSelect = 0 #
curStamp = stampSelect #which stamps to display
tool = "" #which tool is currently in use
wholeCap = screen.copy() #screenshot of the entire screen
wholeScreen = screen.copy() #screenshot of the entire screen
screenCap=screen.subsurface(canvasRect).copy() #screenshot of the canvas
shapeFill=False #if the shapes drawn should be filled or not

while running:
    screen.set_clip((0,0,1200,700))

    mx,my=mouse.get_pos() #mx = mouse X-coordinate, my = mouse Y-coordinate
    mb=mouse.get_pressed() #list of the mousebuttons state (pressed/unpressed)

    if not canvasRect.collidepoint((mx,my)): #if the mouse is not on the canvas, sets the cursor to a hand
        curCursor = 0 
        mouse.set_cursor(cursorList[0])

    else:
        if tool == "pencil": #if the mouse is on the canvas and the pencil tool is used, sets the cursor to a pencil
            curCursor = 1
            mouse.set_cursor((7,7), cursorList[curCursor])
            
        elif tool == "brush":#if the mouse is on the canvas and the brush tool is used, sets the cursor to a brush
            curCursor = 2
            mouse.set_cursor((0,0), cursorList[curCursor])

    if tool == "help": #if help mode is activated
        mouse.set_cursor(cursorList[0])
        
        screen.blit(wholeCap, (0,0)) #sets the screen to before the help button was pressed
        
        if pencilRect.collidepoint((mx,my)): #displays the corresponding image and text depending on which tool is being hovered over
            screen.blit(bubble1, (80,-20))
            blitText(infoFont, "This is the pencil tool.", 140,50, BLACK)
            blitText(infoFont, "This tool can have up to a", 130,70, BLACK)
            blitText(infoFont, "width of 3 px.", 170, 90, BLACK)
            
        elif eraserRect.collidepoint((mx,my)):
            screen.blit(bubble1, (80,80))
            blitText(infoFont, "This is the eraser tool.", 140,150, BLACK)
            blitText(infoFont, "This tool will erase in the", 130,170, BLACK)
            blitText(infoFont, "shape of a square.", 170,190, BLACK)

        elif brushRect.collidepoint((mx,my)):
            screen.blit(bubble1, (80,180))
            blitText(infoFont, "This is the brush tool.", 140,250, BLACK)
            blitText(infoFont, "This tool will draw in the", 130, 270, BLACK)
            blitText(infoFont, "shape of a circle.", 170,290, BLACK)

        elif sprayRect.collidepoint((mx,my)):
            screen.blit(bubble1, (80,280))
            blitText(infoFont, "This is the spray can.", 140,350,BLACK)
            blitText(infoFont, 'This tool will "spray" in', 130, 370,BLACK)
            blitText(infoFont, "the shape of a circle.", 150,390, BLACK)

        elif stampRect1.collidepoint((mx,my)) or stampRect2.collidepoint((mx,my)) or stampRect3.collidepoint((mx,my)):
            screen.blit(bubble2, (800, my//100*100-175))
            blitText(infoFont, "These are the stamps.", 860, my//100*100-150, BLACK)
            blitText(infoFont, "Drag and let go to", 875, my//100*100-125, BLACK)
            blitText(infoFont, "place a stamp!", 890, my//100*100-100, BLACK)

        elif bgRect1.collidepoint((mx,my)) or bgRect2.collidepoint((mx,my)) or bgRect3.collidepoint((mx,my)):
            screen.blit(bubble2, (500, my//100*100-175))
            blitText(infoFont, "These are the backgrounds.", 540, my//100*100-150, BLACK)
            blitText(infoFont, "When you click, ", 585, my//100*100-125, BLACK)
            blitText(infoFont, "the background will change!", 535, my//100*100-100, BLACK)
            
        elif lineRect.collidepoint((mx,my)):
            screen.blit(bubble1, (mx//100*100+30, my//100*100-180))
            blitText(infoFont, "This is the line tool.", mx//100*100+90,  my//100*100-120, BLACK)
            blitText(infoFont, "Drag and let go to draw", mx//100*100+85,  my//100*100-90, BLACK)
            blitText(infoFont, "a line!", mx//100*100+150, my//100*100-60, BLACK)

        elif rectRect.collidepoint((mx,my)):
            screen.blit(bubble1, (mx//100*100+30, my//100*100-180))
            blitText(infoFont, "This is the rect tool.", mx//100*100+90,  my//100*100-120, BLACK)
            blitText(infoFont, "Drag and let go to draw", mx//100*100+85,  my//100*100-90, BLACK)
            blitText(infoFont, "a rect!", mx//100*100+150,  my//100*100-60, BLACK)

        elif ellipseRect.collidepoint((mx,my)):
            screen.blit(bubble1, (mx//100*100+30, my//100*100-180))
            blitText(infoFont, "This is the ellipse tool.", mx//100*100+90,  my//100*100-120, BLACK)
            blitText(infoFont, "Drag and let go to draw", mx//100*100+85,  my//100*100-90, BLACK)
            blitText(infoFont, "an ellipse!", mx//100*100+140,  my//100*100-60, BLACK)
            
        elif clearRect.collidepoint((mx,my)):
            screen.blit(bubble3, (mx//100*100+30, my//100*100+80))
            blitText(infoFont, "This is the clear screen tool", mx//100*100+70,  my//100*100+150, BLACK)
            blitText(infoFont, "Click this button if you want", mx//100*100+65,  my//100*100+170, BLACK)
            blitText(infoFont, "to clear the screen!", mx//100*100+100, my//100*100+190, BLACK)

        elif bucketRect.collidepoint((mx,my)):
            screen.blit(bubble3, (mx//100*100+30, my//100*100+80))
            blitText(infoFont, "This is the paint bucket tool", mx//100*100+70,  my//100*100+150, BLACK)
            blitText(infoFont, "Click this button if you want", mx//100*100+65,  my//100*100+170, BLACK)
            blitText(infoFont, "to fill the screen with a color!", mx//100*100+60, my//100*100+190, BLACK)

        elif saveRect.collidepoint((mx,my)):
            screen.blit(bubble3, (mx//100*100+30, my//100*100+30))
            blitText(infoFont, "This is the save screen tool.", mx//100*100+70,  my//100*100+100, BLACK)
            blitText(infoFont, "Click this button if you want", mx//100*100+65,  my//100*100+120, BLACK)
            blitText(infoFont, "to save the canvas as a file!", mx//100*100+60, my//100*100+140, BLACK)

        elif loadRect.collidepoint((mx,my)):
            screen.blit(bubble3, (mx//100*100+70, my//100*100+70))
            blitText(infoFont, "This is the load image tool.", mx//100*100+105, my//100*100+140, BLACK)
            blitText(infoFont, "Click this button if you want", mx//100*100+95,  my//100*100+160, BLACK)
            blitText(infoFont, "to load an image on the canvas!", mx//100*100+93, my//100*100+180, BLACK)

        elif helpRect.collidepoint((mx,my)):
            screen.blit(bubble4, (mx//100*100-195, my//100*100-185))
            blitText(infoFont, "This is the help button.", mx//100*100-130,  my//100*100-130, BLACK)
            blitText(infoFont, "Click anywhere if you want", mx//100*100-160,  my//100*100-110, BLACK)
            blitText(infoFont, "to turn on/off the help feature!", mx//100*100-170, my//100*100-90, BLACK)

        elif weightRect.collidepoint((mx,my)):
            screen.blit(bubble5, (800, 60))
            blitText(infoFont, "This is the weight button.", 850,  120, BLACK)
            blitText(infoFont, "Click this if you want to type", 830,  140, BLACK)
            blitText(infoFont, "to change the weight!", 850,160,BLACK)

        elif upArrowRect.collidepoint((mx,my)) or downArrowRect.collidepoint((mx,my)):
            screen.blit(bubble5, (850, 60))
            blitText(infoFont, "These buttons", 930,100, BLACK)
            blitText(infoFont, "change weight.", 930,120, BLACK)
            blitText(infoFont, "Click up to increase weight.", 870 ,140, BLACK)
            blitText(infoFont, "Click down to decrease weight.", 870, 160, BLACK)

        elif fillSwitch.collidepoint((mx,my)):
            screen.blit(bubble1, (100,475))
            blitText(infoFont, "This is the fill switch.", 160, 520, BLACK)
            blitText(infoFont, "Click this to fill/unfill shapes.", 130, 550, BLACK)

    if not drawing: #if something is not being drawn currently                   
        if not mb[0] and not mb[1] and not mb[2]: #if the no mouse is being pressed down
            for i in range(21): #checks all the rectangles
                if allRects[i].collidepoint((mx,my)): #if the mouse is hovering over the tool's rect, sets the hover status to True, otherwise False
                    hoverRect[i] = True
                else:
                    hoverRect[i] = False
            

    for evt in event.get(): #event loop
        if evt.type==QUIT: #if the X in the top-right corner is being clicked, ends the program
            running=False
            break

        if evt.type == MOUSEBUTTONDOWN:
            sx, sy = evt.pos #x and y coordinates of when the mouse was pressed down - this will be used for the line, rect, and ellipse tool.
            
            if evt.button == 1 and tool != "" and canvasRect.collidepoint((mx,my)): #Makes sure that a tool is in use and the user is pressing with the left mouse button on the canvas
                drawing = True #sets drawing to True - this boolean will be used so the program knows if the user is in the process of drawing

        if evt.type==MOUSEBUTTONUP:

            if tool == "help": #If this is true, this means that the user clicked their mouse while the help page was active
                tool = "" #resets the tool
                selectRect[10] = False #deselects the help tool
                screen.blit(wholeCap, (0,0)) #brings back the screen where the user last left off before pressing the help button
                screen.blit(screenCap, (150,150)) #brings back the canvas where the user last left off before pressing the help button
                break
            
            screenCap = screen.subsurface(canvasRect).copy() #screenshots the canvas

            if not inRect(mx,my, 100,100,1200,600) and not drawing: #checks if the mouse is in not on the canvas, not on the frame, and not drawing something currently

                for i in range(21): #Loops through all of the tool rectangles
                    if allRects[i].collidepoint((mx,my)): #checks if the mouse is inside one of the tool rects
                        selectRect[i] = True #sets the tool to selected
                            
                        try: #Tries to set the tool to one of the tools, but if the list index is too large, this means that there is no valid tool that corresponds to the rectangle that the mouse is in.
                            #This is done so that the rectangles that aren't for tools can still be outlined for hovering, but when selected, the current tool doesn't change                 
                            tool = tools[i]
                        except: #since the rectangle that the mouse is in doesn't correspond to a tool, the current tool doesn't change
                            1
                            
                        if tool == "stamp1": #sets the currentstamp according to which stamp was selected
                            curStamp = stampSelect
                        if tool == "stamp2":
                            curStamp = stampSelect+1
                        if tool == "stamp3":
                            curStamp = stampSelect+2

                        if "stamp" in tool: #displays the tool as just stamp
                            tool = "stamp"
                    else:
                        selectRect[i] = False #since the mouse was not in the rectangle, sets the selected value to False (that tool isn't selected)

                #This is done to change which stamps in the list are to be displayed as options
                if rightArrowBox.collidepoint((mx,my)):
                    stampSelect += 3 #increases the current stamp and the selected stamps to display by 3
                    curStamp += 3
                   
                if leftArrowBox.collidepoint((mx,my)):
                    stampSelect -= 3 #decreases the current stamp and the selected stamps to display by 3
                    curStamp -= 3
                    
                stampSelect += 12 #makes sure that all values for the curStamp and stampSelect are from 0-11 (inclusive). This is important so that there is no Index out of Bounds error
                stampSelect %= 12
                curStamp += 12
                curStamp %= 12

                #If any of the background boxes are selected, sets the background to the corresponding image
                if bgRect1.collidepoint((mx,my)) or bgRect2.collidepoint((mx,my)) or bgRect3.collidepoint((mx,my)) or bucketRect.collidepoint((mx,my)) or clearRect.collidepoint((mx,my)):
                    tool = ""
                    #resets the tool if the screen is being cleared or a new background is being made
                    
                if bgRect1.collidepoint((mx,my)): 
                    screen.blit(bg1_f, (150,150)) #blits the background image to the canvas
                    screenCap = screen.subsurface(canvasRect).copy() #screenshots the canvas - this is used for the clear feature so that the background is preserved
                    wholeScreen = screen.copy() #screenshots the entire screen - this is used for the eraser tool so that the background is preserved when erasing
                    selectRect[15] = False #deselects the bg1Rect
                    
                elif bgRect2.collidepoint((mx,my)):
                    screen.blit(bg2_f, (150,150))
                    screenCap = screen.subsurface(canvasRect).copy()
                    wholeScreen = screen.copy()
                    selectRect[16] = False

                elif bgRect3.collidepoint((mx,my)):
                    screen.blit(bg3_f, (150,150))
                    screenCap = screen.subsurface(canvasRect).copy()
                    wholeScreen = screen.copy()
                    selectRect[17] = False

                #If the fill bucket is selected, fills the screen with the current color

                elif bucketRect.collidepoint((mx,my)):
                    draw.rect(screen, curColor, canvasRect)
                    screenCap = screen.subsurface(canvasRect).copy()
                    wholeScreen = screen.copy()
                    selectRect[11] = False

                #If the clear feature is selected, sets the canvas to what the last background was (the default is a white canvas)

                elif clearRect.collidepoint((mx,my)):
                    screen.blit(wholeScreen.subsurface(canvasRect), (150,150))
                    screenCap = screen.subsurface(canvasRect).copy()
                    wholeScreen = screen.copy()
                    selectRect[12] = False

                #If the save feature is selected, prompts for a filename with Tkinter

                elif saveRect.collidepoint((mx,my)):
                    selectRect[13] = False #deselects the save feature
                    fname = filedialog.asksaveasfilename(defaultextension=".png") #default extension is png so if the user doesn't put their own extension, it will automatically be a png
                    try: #this is done to save only valid file names - empty string (when the user hits cancel instead of inputting a file name) is invalid so the program will do nothing
                        image.save(screen.subsurface(canvasRect), fname)
                        
                    except:
                        1

                #If the load feature is selected, prompts for a file with Tkinter
        
                elif loadRect.collidepoint((mx,my)):
                    selectRect[14] = False #deselects the load feature
                    fname = filedialog.askopenfilename()
                    try: #this is here to prevent invalid file types from being blitted
                        img =image.load(fname)
                        img = transform.scale(img, (min(1000, img.get_width()), min(400, img.get_height()))) #makes sure the image width and height doesn't exceed the canvas
                        screen.blit(wholeScreen.subsurface(canvasRect), (150,150)) #sets the background
                        screen.blit(img, (150,150)) #blits the selected image

                    except: #since the file was invalid, nothing happens
                        1

                elif fillSwitch.collidepoint((mx,my)): #Toggles On/Off for the shapeFill. Also displays the correct text for ON/OFF
                    
                    if shapeFill: #If the shapeFill is on, turns it off
                        draw.rect(screen, RED, fillSwitch)
                        shapeFill = False
                        blitText(sizeFont, "OFF", fillSwitch[0]+10, fillSwitch[1], BLACK)
                        
                    else:#If the shapeFill is off, turns it on
                        draw.rect(screen, GREEN, fillSwitch)
                        shapeFill = True
                        blitText(sizeFont, "ON", fillSwitch[0]+15, fillSwitch[1], BLACK)

                elif weightRect.collidepoint((mx,my)): #If the box to change the weight is selected
                    if typingFont: #If the user was previously in typing mode, turns it off and makes sure the weight is at least 1
                        typingFont = False
                        if sz == 0:
                            sz = 1
                    else: #Otherwise, turns typing mode on
                        typingFont = True

                    #In "typing mode", the user will be able to use the numbers, BACKSPACE, and RETURN to change sz (the weight) as long as sz < 100 and there are no floating point values

                if upArrowRect.collidepoint((mx,my)): #If the uparrowrect is selected, increases the weight by 1 to a maximum of 99
                    sz = min(99, sz+1)
                if downArrowRect.collidepoint((mx,my)): #If the downarrowrect is selected, decreases the weight by 1 to a minimum of 1
                    sz  = max(1, sz-1)

            
            drawing = False #The mouse was released, so the user has stopped drawing for now
            #DRAWING TOOLS
            if tool == "line":
                screen.set_clip(canvasRect)
                screen.blit(screenCap,(150,150))
                
                draw.line(screen,curColor,(sx,sy),(mx,my), sz)
                screenCap=screen.subsurface(canvasRect).copy()
                screen.blit(screenCap, (150,150))
                screen.set_clip((0,0,1200,700))

            elif tool == "rect":
                screen.set_clip(canvasRect)
                screen.blit(screenCap,(150,150))
                drawRect = Rect(sx, sy, mx-sx, my-sy)
                drawRect.normalize()
                drawRectangle(drawRect, sz)
                screenCap=screen.subsurface(canvasRect).copy()
                screen.blit(screenCap, (150,150))
                screen.set_clip((0,0,1200,700))

            elif tool == "ellipse":
                screen.set_clip(canvasRect)
                screen.blit(screenCap,(150,150))
                drawRect = Rect(sx, sy, mx-sx, my-sy)
                drawRect.normalize()
                drawEllipse(drawRect)
                screenCap=screen.subsurface(canvasRect).copy()
                screen.blit(screenCap, (150,150))
                screen.set_clip((0,0,1200,700))

            elif tool == "stamp":
                screen.set_clip(canvasRect)
                screen.blit(screenCap, (150,150))
                stampPic = stamps[curStamp]
                screen.blit(stampPic, (mx-(stampPic.get_width()//2), my-(stampPic.get_height()//2)))
                screenCap=screen.subsurface(canvasRect).copy()
                screen.blit(screenCap, (150,150))
                screen.set_clip((0,0,1200,700))

        #Checking if the user is typing something on the keyboard and typing mode is active
        if evt.type == KEYUP and typingFont:

            if evt.key == K_RETURN: #If the user presses K_RETURN, then typing mode is set off because this marks the end of th euser typing.
                
                typingFont = False
    
            for i in range(47, 58):
                if evt.key == i:
                    if sz == 0:
                        sz = ""
                    if int(str(sz)+str(i-48)) < 100:
                        sz = str(sz)+str(i-48)
                        sz = int(sz)

            if evt.key == 8: #8 is the ASCII value for backspace
                if sz < 10: #If the size is <10, there is only one digit, so the size is set to 0
                    sz = 0

                else:
                    sz = str(sz) #makes the sz (originally an integer) to a string
                    sz = sz[0] #removes the second digit of the number so it's just the tens digit
                    sz = int(sz) #converts the string back to an integer


    #COLOR SLIDERS
    draw.rect(screen, RED, (820,25, 90,10))
    draw.rect(screen, GREEN, (820,45, 90,10))
    draw.rect(screen, BLUE, (820,65, 90,10))

    
    #MAKE THE SLIDER ACTUALLY SLIDE 

    if mb[0] and not drawing: #if mouse is pressed and no tools are in use

        #check if the mouse is on one of the sliders and if it is, moves the curR/curG/curB value relative to how far along the slider the mouse is

        if inRect(mx, my, 820,25,910,35): #Red slider
            curR = int((mx-820)*255/90) #(mx-820) sets the value to something from 0-90, the *255/90 part sets the value from 0-255
            
        elif inRect(mx,my, 820,45,910,55): #Blue slider
            curG = int((mx-820)*255/90)
        elif inRect(mx,my, 820,65,910,75): #Green slider
            curB = int((mx-820)*255/90)

    draw.rect(screen, GREY, (820+int(curR)/255*80, 25, 10,10)) #Draws the sliders as GREY rectangles on the slider depending on how far along the sliders are
    #+820 is to set the x value to be at least 820, int(curR)/255*80 gets how far along the slider should be, keeping in mind the max value for x should be 900 because that is the top left corner of the rectangle
    draw.rect(screen, GREY, (820+int(curG)/255*80, 45, 10,10))
    draw.rect(screen, GREY, (820+int(curB)/255*80, 65, 10,10))

    for i in range(25,66,20): #WHITE rectangles so the text is more visible
        draw.rect(screen, WHITE, (930, i, 65, 10))
        
    #Shows the user how much R, G, B the current color has
    numPic = colorFont.render(str(curR), 1, RED)
    screen.blit(numPic, (945 - numPic.get_width()//2,25))
    numPic = colorFont.render(str(curG), 1, GREEN)
    screen.blit(numPic, (945 - numPic.get_width()//2,45))
    numPic = colorFont.render(str(curB), 1, BLUE)
    screen.blit(numPic, (945 - numPic.get_width()//2,65))

    blitText(colorFont, "RED", 960,25, RED)
    blitText(colorFont, "GREEN", 960,45, GREEN)
    blitText(colorFont, "BLUE", 960,65, BLUE)

    curColor = (int(curR), int(curG), int(curB)) #sets the current color as (curR, curG, curB)
    draw.rect(screen, curColor, (1010,25, 50,50)) #draws a rectangle to show which color is currently selected

    #WEIGHT OF TOOLS

    draw.rect(screen, WHITE, weightRect)
    draw.rect(screen, GREEN, upArrowRect)
    draw.rect(screen, RED, downArrowRect)

    screen.blit(board, (800,600))
    draw.rect(screen, GREEN, rightArrowBox)
    screen.blit(rightArrowIcon, (rightArrowBox[0], rightArrowBox[1]-5))
    draw.rect(screen, RED, leftArrowBox)
    screen.blit(leftArrowIcon, (leftArrowBox[0], leftArrowBox[1]-5))
    screen.blit(qmark, (helpRect[0]-25, helpRect[1]+10))

    #draws 3 stamps at a time

    screen.blit(stamps[stampSelect], (825, 615))
    for i in range(1,3):
        screen.blit(stamps[stampSelect+i], (850-(stamps[stampSelect+i].get_width()//2) + 100*i, 600))

    for i in range(21): #Goes through all of the rectangles
        if selectRect[i]: #If the rectangle is selected, outlines it with RED
            draw.rect(screen, RED, allRects[i], 2)
        elif hoverRect[i]: #If the rectangle is being hovered over, outlines it with BLUE
            draw.rect(screen, BLUE, allRects[i], 2)
        else: #If the rectangle is neither selected nor hovered over, outlines it with WHITE
            draw.rect(screen, WHITE, allRects[i], 2)

    if typingFont: #If the user is in typing mode, draws a GREEN outline around the typebox
        draw.rect(screen, GREEN, weightRect, 1)


    szPic= sizeFont.render(str(sz), 1, BLACK) #show the user the current weight of the tools
    screen.blit(szPic, (1100-szPic.get_width()//2,50-szPic.get_height()//2))

    if canvasRect.collidepoint((mx,my)) and mb[0]: #This verifies that the left mouse is being pressed down and that the mouse is on the canvas
        sz = max(sz, 1) #makes sure the size is at least 1
        if tool == "pencil" or tool == "spray" or tool == "brush" or tool == "eraser":
            screen.set_clip(canvasRect) #makes it so only the canvasRect gets updated
            
        if tool == "pencil":
            sz = min(sz, 3) #since the pencil is in use, the maximum weight is 3
            draw.line(screen, curColor, (mx,my), (pmouseX, pmouseY), sz) #draws a line from the current mouse position to the previous mouse position with the weight of sz

        if tool == "spray": 
            rx = randint(mx-sz, mx+sz) #picks random x value within the square that can be defined as Rect(mx,my,sz,sz)
            ry = randint(my-sz, my+sz) #picks random y value within the square that can be defined as Rect(mx,my,sz,sz)
            if inCircle(rx, ry, mx, my, sz): #If the randomly selected x and y values are in the circle with center=(mx,my) and radius = sz, draws a circle at that location
                draw.circle(screen, curColor, (rx,ry), 1)

        if tool == "brush":

            deltaX = pmouseX-mx #Change in x between the previous mouseX value and current mouseX value
            
            if deltaX == 0: #If the change in x is 0, sets it to 1 so that there is no division by 0 error
                deltaX = 1

            deltaY = pmouseY-my #Change in y between the previous mouseY value and the current mouseY value

            slope = deltaY/deltaX #the slope in slope-intercept form is deltaY/deltaX. Here, there is no division by 0 error because deltaX would be set to 1 if necessary

            B = my - slope*mx #solving for the y-intercept of this line where the slope is the variable named slope

            #The idea is to iterate through all the points between pmouseX and mx and using the equation of the line, find the correct y coordinate to draw the circle

            change = -1 #If mx > pmouseX, the loop will start at mx and decrease by 1 to pmouseX
            if pmouseX > mx: #If pmouseX > mx, the loop will start at mx and increase by 1 to pmouseX
                change = 1
            
            for i in range(mx, pmouseX, change): #iterates through all the x coordinates between mx and pmouseX
                draw.circle(screen, curColor, (i, i*slope+B), sz) #draws a circle with radius sz around each point on the line with the equation y = slope*x + B

            #The idea is to iterate through all the points between pmouseY and my and using the equation of the line, find the correct x coordinate to draw the circle

            change = -1 #If my > pmouseY, the loop will start at my and decrease by 1 to pmouseY
            if pmouseY > my:#If pmouseY > my, the loop will start at my and increase by 1 to pmouseY
                change = 1
                
            for i in range(my, pmouseY, change): #iterates through all the y coordinates between my and pmouseY
                draw.circle(screen, curColor, ((i-B)/slope, i), sz) #since the line has the equation y= slope*x + B, x = (y-B)/slope
                
        if tool == "eraser":

            #The concept of the eraser is very similar to the brush but instead of drawing a circle, blit a screenshot (square) of the background 

            deltaX = pmouseX-mx
            if deltaX == 0:
                deltaX = 1
            slope = (pmouseY-my)/deltaX

            B = my - slope*mx
            
            change = -1
            if pmouseX > mx:
                change = 1

            ### FIX SO THAT YOU CAN ERASER ON EDGE OF CANVAS WITH LARGE VALUES FOR ERASER

            for i in range(mx, pmouseX, change): #iterating through the x coordinates

                replacePic = wholeScreen.subsurface((-(sz/(2**0.5))+i,(-(sz/(2**0.5))+my),int(min(sz/(2**0.5)*2, width-(-(sz/(2**0.5))+i))),int(min((sz/(2**0.5)*2), height-(-(sz/(2**0.05)))+my)))).copy() #The background picture to blit making sure that the proposed screenshot is in wholeScreen
                screen.blit(replacePic, (-(sz/(2**0.5))+i,-(sz/(2**0.5))+my)) #blits the replacePic in the appropriate location so that the mouse is in the center of the square0

            change = -1
            if pmouseY > my:
                change = 1
                
            for i in range(my, pmouseY, change): #iterating throught the y coordinates
                X = int((i-B)/slope)
                try: #make sure that the screenshot is valid 
                    replacePic = wholeScreen.subsurface((-(sz/(2**0.5))+X,-(sz/(2**0.5))+i,sz/(2**0.5)*2,sz/(2**0.5)*2))
                except: #the screenshot is off the screen, so it can't screenshot
                    1
                screen.blit(replacePic, (-(sz/(2**0.5))+X,-(sz/(2**0.5))+i))
                
    if mb[0]:
        if tool == "line" or tool == "rect" or tool == "ellipse" or tool == "stamp": #makes it so only the canvasRect gets updated
            screen.set_clip(canvasRect)
            screen.blit(screenCap, (150,150))
            
        if tool == "line":
            draw.line(screen,curColor,(sx,sy),(mx,my), sz) #draws a line from where the mouse started when it was pressed to where the mouse is now

        if tool == "rect":
            drawRect = Rect(sx, sy, mx-sx, my-sy)
            drawRect.normalize() 
            drawRectangle(drawRect, sz) #draws a rectangle from where the mouse started when it was pressed to where the mouse is now

        if tool == "ellipse":
            
            drawRect = Rect(sx, sy, mx-sx, my-sy)
            drawRect.normalize()
            drawEllipse(drawRect) #draws an ellipse from where the mouse started when it was pressed to where the mouse is now

        if tool == "stamp":
            stampPic = stamps[curStamp] #the current stamp that is selected
            screen.blit(stampPic, (mx-(stampPic.get_width()//2), my-(stampPic.get_height()//2))) #draws a stamp where the mouse is now
            
    screen.blit(board.subsurface(0,0, 100,100), (0,500)) #Clears the part of the screen where the name of the tool will go
    blitText(sizeFont, "Tool: ", 0, 500, BLACK) 
    toolPic = selectFont.render(tool, 1, BLACK)
    screen.blit(toolPic, (50-toolPic.get_width()//2, 560)) #blits the current tool in use

    screen.blit(board.subsurface(0,0,100,100), (0,600)) #Clears the part of the screen where the X and Y coordinates will be blitted
    blitText(sizeFont, "X:", 5,600, BLACK)
    blitText(sizeFont, "Y:", 5,650, BLACK)
    
    if canvasRect.collidepoint((mx,my)): #If the mouse is on the canvas, shows the location relative to where it is on the canvas
        XPic = selectFont.render(str(mx-150), 1, BLACK)
        screen.blit(XPic, (75-(XPic.get_width()//2), 610))
        YPic = selectFont.render(str(my-150), 1, BLACK)
        screen.blit(YPic, (75-(YPic.get_width()//2), 660))

    pmouseX, pmouseY = mx, my #the previous mouse location for the next time the loop goes around
    display.flip()

quit() #ends the program
