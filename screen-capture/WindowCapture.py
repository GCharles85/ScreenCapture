import numpy as np
import win32gui, win32ui, win32con

class WindowCapture:
    # define monitor width and height
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    def __init__(self, window_name):
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))

        #get window dimensions and get rid of black borders
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0] #the 0th and 1th index are the x and y coordinates of the top left corner of the window
        self.h = window_rect[3] - window_rect[1] #the 2nd and 3rd index are the x and y coordinates of the bottom right corner of the window

        # account for the window border and titlebar and cut them off
        border_pixels = 8
        titlebar_pixels = 30   
        self.w = self.w - (border_pixels * 2) # subtract 2 times the width from left and right border
        self.h = self.h - titlebar_pixels - border_pixels # subtract the height of the titlebar and the height of the titlebar
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def get_screenshot(self):
        ''' get the window image data '''
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.h, self.w)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.h, self.w), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        #save the screenshot
        #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.w, self.h, 4)

        #free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # drop the alpha channel, or cv.matchTemplate() will throw an error like:
        # error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type() && _img.dims() <= 2 in function 'cv::matchTemplate'
        img = img[...,:3]

        # make image C_CONTIGUOUS to avoid an error that looks like:
        # File ... in draw_rectangles
        # TypeError: an integer is required (got type tuple)
        # see the discussion here:
        # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
        img = np.ascontiguousarray(img)

        return img
    
    def get_screen_position(self, pos):
        ''' translate a position on the window screenshot to a position on the screen '''
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)