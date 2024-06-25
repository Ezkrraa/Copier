import pynput, pyautogui, keyboard, pyperclip
import os, sys, codecs, time

# edit to change the amount of characters allocated per book
# estimate based off average text
chars_per_page = 250

# pages per book, java has 100, bedrock has 50
pages_per_book = 100


def printBook(book: list[str], next_mouse_btn_pos: tuple[int, int], prev_mouse_btn_pos: tuple[int, int]):
    mouse = pynput.mouse.Controller()
    for page in book:
        pyperclip.copy(page.strip())
        # time.sleep(0.1)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.10)
        mouse.position = next_mouse_btn_pos
        time.sleep(0.1)
        mouse.click(pynput.mouse.Button.left)

    mouse.position = prev_mouse_btn_pos
    time.sleep(0.1)
    mouse.click(pynput.mouse.Button.left, 99)


def awaitKeyPress() -> None:
    output = False

    def on_release(key):
        if key == pynput.keyboard.Key.enter:
            listener.stop()
            output = True
        elif key == pynput.keyboard.Key.backspace:
            output = False

    listener = pynput.keyboard.Listener(on_release=on_release)
    listener.start()
    # make it blocking
    listener.join()


def interruptListener():
    "will make app crash at pressing backspace."

    def callback(key):
        if key == pynput.keyboard.Key.backspace:
            print("\nBackspace pressed. Exiting.")
            os._exit(1)

    return callback


def getMousePosition() -> tuple[int, int]:
    """returns the place where right mouse button gets clicked, BLOCKING"""
    xPos = 0
    yPos = 0

    def on_click(x, y, button, pressed):
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


def readFile(filePath: str):
    if os.path.exists(filePath):
        try:
            file = codecs.open(filePath, encoding="utf-8", errors="strict")
            return file.read().replace("\n", " ").replace("  ", " ").replace("  ", " ").replace("\t", "")
        except UnicodeDecodeError:
            input("This file seems like it's not valid UTF-8. ")
            return ""
        except FileNotFoundError:
            input("This file doesn't seem to exist. ")
            return ""


def splitString(string: str, n: int) -> list[str]:
    """splits a string into a list of strings, each with length n,
    last one can be shorter."""
    return [(string[i : i + n]) for i in range(0, len(string), n)]


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def mainloop():
    while True:
        clear()
        print(
            "This is Sav's copier script for minecraft books.\nPlease enter the name of the file you want to copy + paste.\nIt should be in the folder of this program to work.\nKeep minecraft windowed to be able to see both this and the program.\nPress [Backspace] at any point to stop."
        )
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

        if len(allText) > (chars_per_page * pages_per_book):
            books = splitString(allText, (chars_per_page * pages_per_book))
            print(f"This file is {len(books)} books long.\n[Enter to continue]")

            for i in range(len(books)):
                input(f"This is book {i+1}/{len(books)}.\nAfter pressing Enter, printing will start in 5s.")
                time.sleep(5)
                printBook(splitString(books[i], chars_per_page), next, prev)
                clear()

        else:
            allText = splitString(allText, 260)
            input("After pressing Enter, printing will start in 5s.")
            time.sleep(5)
            printBook(allText, next, prev)


if __name__ == "__main__":
    keyboard.hook(interruptListener())
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
