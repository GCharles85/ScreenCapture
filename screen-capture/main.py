import cv2 as cv
import numpy as np
import os
import pyautogui

while(True):

    screenshot = pyautogui.screenshot()

    cv.imshow('Computer Vision', screenshot)

    # press q with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')