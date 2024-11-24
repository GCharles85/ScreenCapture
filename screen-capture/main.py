import cv2 as cv
import numpy as np
import os
from time import time
import win32con, win32ui, win32gui

def window_capture():
    
    hwnd = None
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, 1920, 1080)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (1920, 1080), dcObj, (0, 0), win32con.SRCCOPY)

    #save the screenshot
    dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')

    #free resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())


loop_time = time()
'''
while(True):


    screenshot = ImageGrab.grab() #cuts out dependencies as opposed to pyautogui.screenshot(), makes fps go up
    screenshot = np.array(screenshot)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

    cv.imshow('Computer Vision', screenshot)
    
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press q with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
'''
window_capture()
print('Done.')