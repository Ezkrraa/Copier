import pynput, pyautogui, keyboard, pyperclip
import os, codecs, time
from math import ceil

import splitter


# pages per book, java has 100, bedrock has 50
PAGES_PER_BOOK = 100


def printBook(book: list[list[str]], next_mouse_btn_pos: tuple[int, int], prev_mouse_btn_pos: tuple[int, int]):
    mouse = pynput.mouse.Controller()
    for page in book:
        page_txt = " ".join(page)
        pyperclip.copy(page_txt.strip())
        # time.sleep(0.1)
        pyautogui.hotkey("ctrl", "v")
        # time.sleep(0.10)
        mouse.position = next_mouse_btn_pos
        # time.sleep(0.1)
        mouse.click(pynput.mouse.Button.left)

    mouse.position = prev_mouse_btn_pos
    time.sleep(0.03)
    mouse.click(pynput.mouse.Button.left, 99)


def awaitKeyPress() -> None:
    def on_release(key):
        if key == pynput.keyboard.Key.enter:
            listener.stop()

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
        if pressed and button == pynput.mouse.Button.middle:
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


# def splitString(string: str, n: int) -> list[str]:
#     """splits a string into a list of strings, each with length n,
#     last one can be shorter."""
#     return [(string[i : i + n]) for i in range(0, len(string), n)]


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
        all_text = readFile(filePath)
        if all_text == None:
            continue

        pages = splitter.split_into_pages_and_lines(all_text)
        if len(pages) > PAGES_PER_BOOK:
            print(f"File was read. It is {ceil(len(pages) / 100)} books long.")
        else:
            print("File was read successfully.")
        print("Please middle-click the 'next page' button in minecraft.")
        next = getMousePosition()
        print("Please middle-click the 'previous' button in minecraft.")
        prev = getMousePosition()

        if len(pages) > PAGES_PER_BOOK:
            # handle multiple books
            for i in range(0, len(pages), PAGES_PER_BOOK):
                input(f"This is book {i//100+1}/{ceil(len(pages) / 100)}.\nAfter pressing Enter, printing will continue in 5s.")
                time.sleep(5)
                # don't roll over into the start again
                end = min(i + 100, len(pages))
                printBook(pages[i:end], next, prev)
                clear()
        else:
            input("After pressing Enter, printing will start in 5s.")
            time.sleep(5)
            printBook(pages, next, prev)


if __name__ == "__main__":
    keyboard.hook(interruptListener())
    mainloop()
