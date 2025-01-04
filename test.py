import ctypes
import tkinter
from ctypes import wintypes
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import os
import subprocess
import threading

class BITMAP(ctypes.Structure):
    _fields_ = [
        ("bmType", wintypes.LONG),
        ("bmWidth", wintypes.LONG),
        ("bmHeight", wintypes.LONG),
        ("bmWidthBytes", wintypes.LONG),
        ("bmPlanes", wintypes.WORD),
        ("bmBitsPixel", wintypes.WORD),
        ("bmBits", wintypes.LPVOID),
    ]

def extract_icon(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    large, small = wintypes.HICON(), wintypes.HICON()
    num_icons = ctypes.windll.shell32.ExtractIconExW(file_path, 0, ctypes.byref(large), ctypes.byref(small), 1)

    if num_icons > 0 and large:
        hicon = large.value
        hdc = ctypes.windll.user32.GetDC(None)
        hbmp = ctypes.windll.gdi32.CreateCompatibleBitmap(hdc, 32, 32)
        hdc_mem = ctypes.windll.gdi32.CreateCompatibleDC(hdc)
        hbm_old = ctypes.windll.gdi32.SelectObject(hdc_mem, hbmp)
        ctypes.windll.user32.DrawIconEx(hdc_mem, 0, 0, hicon, 32, 32, 0, None, 0x0003)
        ctypes.windll.gdi32.SelectObject(hdc_mem, hbm_old)
        ctypes.windll.gdi32.DeleteDC(hdc_mem)
        ctypes.windll.user32.ReleaseDC(None, hdc)

        bmpinfo = BITMAP()
        ctypes.windll.gdi32.GetObjectW(hbmp, ctypes.sizeof(bmpinfo), ctypes.byref(bmpinfo))

        bmpstr = ctypes.create_string_buffer(bmpinfo.bmWidthBytes * bmpinfo.bmHeight)
        ctypes.windll.gdi32.GetBitmapBits(hbmp, bmpinfo.bmWidthBytes * bmpinfo.bmHeight, bmpstr)

        image = Image.frombuffer("RGBA", (bmpinfo.bmWidth, bmpinfo.bmHeight), bmpstr, "raw", "BGRA", 0, 1)
        png_path = os.path.splitext(file_path)[0] + ".png"
        image.save(png_path)

        ctypes.windll.gdi32.DeleteObject(hbmp)
        ctypes.windll.user32.DestroyIcon(hicon)

        return png_path
    return None

def create_photo_image(file_path):
    png_path = extract_icon(file_path)
    if png_path:
        img = Image.open(png_path)
        photo = ImageTk.PhotoImage(img)
        return photo
    else:
        return None


def run_program(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    try:
        # Sử dụng subprocess để chạy chương trình
        subprocess.Popen([file_path])
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the program: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
    return file_path

def on_select_file(button):
    file_path = select_file()
    if file_path:
        photo = create_photo_image(file_path)
        button.config(image=photo, command=lambda: threading.Thread(target=run_program, args=(file_path,)).start())
        button.image = photo  # Keep a reference to avoid garbage collection


root = tk.Tk()

photolabels = [tk.Button(root, bg="#eeeeee", bd=0) for _ in range(6)]

for btn in photolabels:
    btn.pack()

addLabel = tk.Button(root, text="Add an exe app!!", bg="blue", command=lambda: on_select_file(next(btn for btn in photolabels if btn['image'] == '')))
addLabel.pack()

root.mainloop()