import pyautogui
from tkinter import *
import requests
import pyperclip
import io


API = "https://api.api-ninjas.com/v1/imagetotext"

class ScreenshotSelector:
    def __init__(self, master):
        self.master = master
        self.master.attributes('-fullscreen', True)  
        self.master.configure(cursor='cross')  
        self.master.wait_visibility(window)
        self.master.wm_attributes("-alpha", 0.5)
        self.sx = None
        self.sy = None
        self.rect = None

        
        self.master.bind('<ButtonPress-1>', self.on_button_press)
        self.master.bind('<B1-Motion>', self.on_mouse_drag)
        self.master.bind('<ButtonRelease-1>', self.on_button_release)
        self.master.bind('<Escape>', self.cancel)

        
        self.canvas = Canvas(self.master, bg='grey')
        self.canvas.pack(fill=BOTH, expand=True)

    def on_button_press(self, e):
        self.sx = e.x
        self.sy = e.y
        
        self.rect = self.canvas.create_rectangle(self.sx, self.sy, self.sx, self.sy, outline='black', fill='white', stipple='gray25')

    def on_mouse_drag(self, e):
        
        self.canvas.coords(self.rect, self.sx, self.sy, e.x, e.y)

    def on_button_release(self, e):
        
        x1 = min(self.sx, e.x)
        y1 = min(self.sy, e.y)
        x2 = max(self.sx, e.x)
        y2 = max(self.sy, e.y)

        self.master.destroy()

        
        region = (x1, y1, x2 - x1, y2 - y1)
        screenshot = pyautogui.screenshot(region=region)
        
        

        bytesIO = io.BytesIO()
        screenshot.save(bytesIO, format='PNG')
        bytesIO.seek(0)

        files = {'image': bytesIO}
        r = requests.post(API, files=files)

        copy = ""


        if r.status_code == 200:
            words = r.json()

            for line in words:
                copy += line['text'] + " "

            
            print(copy)
            pyperclip.copy(copy)

        else:
            print(f"Error: {r.status_code} - {r.text}")


        
        

    def cancel(self, event):
        self.master.destroy()


window = Tk()
selector = ScreenshotSelector(window)
window.mainloop()
