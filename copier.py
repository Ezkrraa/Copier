import pynput, pyautogui, keyboard
import os, sys, codecs, time, threading



def printBook(book:[str], next:(int, int), prev:(int, int)):
    mouse = pynput.mouse.Controller()
    for page in book:
        pyautogui.write(page, interval=0.005)
        mouse.position = next
        mouse.click(pynput.mouse.Button.left)
    for i in range(len(book)):
        mouse.position = prev
        mouse.click(pynput.mouse.Button.left)


def awaitKeyPress() -> bool:
    output = False
    def on_release(key):
        if(key == pynput.keyboard.Key.enter):
            listener.stop()
            output = True
        elif(key == pynput.keyboard.Key.esc):
            output = False
    listener = pynput.keyboard.Listener(on_release=on_release)
    listener.start()
    # make it blocking
    listener.join()


def interruptListener(keyname):
    '''will make app crash at pressing Esc. not functional.'''
    def callback(key):
        if key.name == keyname:
            print("\nEsc pressed. Exiting.")
            os._exit(1)
    return callback


def getMousePosition() -> (int, int):
    '''returns the place where right mouse button gets clicked, BLOCKING'''
    xPos = 0
    yPos = 0
    def on_click(x, y, button, pressed) -> (int, int):
        if pressed and button == pynput.mouse.Button.right:
            nonlocal xPos, yPos
            xPos, yPos = controller.position
            listener.stop()

    controller = pynput.mouse.Controller()
    listener = pynput.mouse.Listener(on_click=on_click)
    listener.start()
    listener.join()
    return (xPos, yPos)

# I'm making a script to print books automatically
# I'm making it calibrate mouse positions now
# so I can automatically flip book pages too



def readFile(filePath:str):
    if os.path.exists(filePath):
        try:
            file = codecs.open(filePath, encoding="utf-8", errors="strict")
            return file.read().replace("\n", " ")
        except UnicodeDecodeError:
            input("This file seems like it's not valid UTF-8. ")
            return None
        except FileNotFoundError:
            input("This file doesn't seem to exist. ")
            return None


def splitString(input:str, n:int) -> [str]:
    '''splits a string into a list of strings, each with length n,
    last one can be shorter.'''
    return [ (input[ i : i + n ]) for i in range(0, len(input), n )]
    

def mainloop():
    while(True):
        if os.name == "nt":
            os.system('cls')
        else:
            os.system('clear')
        print("This is Sav's copier script for minecraft books.\nPlease enter the name of the file you want to copy + paste.")
        filePath = input("File name: ")
        allText = readFile(filePath)
        if allText == None:
            continue
        elif allText == "":
            input("This is an empty file, try again.")
            continue


        print("File was read.")
        print("Please right-click the 'next page' button in minecraft.")
        next = getMousePosition()
        print("Please right-click the 'previous' button in minecraft.")
        prev = getMousePosition()
        print("Printing starts in 5 seconds.")
        time.sleep(5)

        allText = splitString(allText, 260)
        if len(allText) > 25_500:
            print("This is longer than 1 minecraft book.")
            input("This isn't implemented, try again")
            continue
            # start of implementation
            listText = splitString(allText, 25_500)
            for book in listText:
                book = splitString(book, 255)
                for page in book:
                    pyautogui.typewrite(page)
                    mouse
        else:
            printBook(allText, next, prev)


    
'''
ices. In sit amet ligula id nunc scelerisque ultrices. Mauris sed ex est. Aliquam tempor scelerisque risus at posuere. Curabitur vestibulum magna sed justo fermentum, vitae euismod diam mattis. Quisque aliquam tellus vel nisi tincidunt, vitae ultricies au'''
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
# ..............................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................
# ∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞
if(__name__ == "__main__"):
    keyboard.hook(interruptListener('esc'))
    mainloop()


# TODO:
# 
# 1. Interruptlistener
#    
# 2. Fix getMousePosition 
#     should return a mouse position (x, y), which will get used to calibrate next n prev buttons
#     works!!
# 3. pasting
#     156.066s for 10_000 chars. seems fast enough to me
# 
# 