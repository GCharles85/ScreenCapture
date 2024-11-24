import win32gui, win32ui, win32con

class GetWindows:
    def __init__(self):
        self.windows = []

    def getWindows(self):
        self.windows = []
        win32gui.EnumWindows(self._enumWindowsProc, 0)
        return self.windows

    def _enumWindowsProc(self, hwnd, lParam):
        if not win32gui.IsWindowVisible(hwnd):
            return
        window = {}
        window['hwnd'] = hwnd
        window['title'] = win32gui.GetWindowText(hwnd)
        window['rect'] = win32gui.GetWindowRect(hwnd)
        self.windows.append(window)

print(GetWindows().getWindows())