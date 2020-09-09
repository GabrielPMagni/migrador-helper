from time import sleep
import pyautogui as macro
sleep(15)
for i in range(30000):
    macro.press('f2')
    macro.hotkey('ctrl', 'home')
    macro.press('\'')
    macro.press('tab')
