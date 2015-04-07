import autopy
import time

# needed for keylogger
import pythoncom
import pyHook
import sys


def OnKeyboardEvent(event):
    print('Key:', event)
    return True


def hello():
    while True:
        time.sleep(0.02)
        autopy.mouse.click()


def main():
    # hm = pyHook.HookManager()
    # hm.KeyDown = OnKeyboardEvent
    # hm.HookKeyboard()
    # pythoncom.PumpMessages()

    hello()

if __name__ == '__main__':
    main()
