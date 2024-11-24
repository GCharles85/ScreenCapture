import cv2 as cv
import os
from time import time
from WindowCapture import WindowCapture

wincap = WindowCapture("Byzantine Faults in Sensor Networks - Google Chrome")
loop_time = time()

while(True):
    screenshot =  wincap.get_screenshot() #cuts out dependencies as opposed to pyautogui.screenshot(), makes fps go up
   

    cv.imshow('Computer Vision', screenshot)
    
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press q with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break


print('Done.')