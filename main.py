import tkinter
from tkinter import ttk

import platform  # Use to get operating system info
import psutil  # Use to get computer info

import subprocess
import webbrowser as wb

# Brightness:
import screen_brightness_control

# Audio:
from ctypes import cast
from ctypes import POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities # Use to get the device's speaker
from pycaw.pycaw import IAudioEndpointVolume # Use to change the speaker's volume

# Head
window = tkinter.Tk()
window.geometry("850x500")
window.title("Software")
window.resizable(False, False)
window.config(bg="#000000")

# Body
Body = tkinter.Frame(window, width=850, height=500, bg="#888888")
Body.pack(padx=20, pady=20)

# -------------------LEFT FRAME--------------------------------
LeftFrame = tkinter.Frame(Body, width=310, height=435, bg="#ffffff", highlightthickness=2,
                          highlightbackground="#333333")
LeftFrame.place(x=10, y=10)


# Functions:
def update_available_ram():
    RAM_INFO = psutil.virtual_memory() # Get the device's RAM information

    total_RAM = RAM_INFO.total / 1e9
    available_RAM = RAM_INFO.available / 1e9
    strvar_availableRAM.set(f"Available RAM: {round(available_RAM, 2)}/{round(total_RAM, 2)} GB")
    RAMLabel.after(1000, update_available_ram)


# Laptop image
LaptopImage = tkinter.PhotoImage(file="./image/laptop/laptop.png")
photo_laptopLabel = tkinter.Label(LeftFrame, image=LaptopImage, bg="#ffffff")
photo_laptopLabel.place(x=2, y=20)

# Get system information (OS and computer's configuration)
mySystem = platform.uname()

computerNameLabel = tkinter.Label(LeftFrame, text=mySystem.node, font=("Acumin Variable Concept", 15, "bold"),
                                  bg="#ffffff")
computerNameLabel.place(x=55, y=200)

OSNameLabel = tkinter.Label(LeftFrame, text=f"Operating System: {mySystem.system} {mySystem.release}",
                            font=("Acumin Variable Concept", 9), bg="#ffffff")
OSNameLabel.place(x=15, y=230)

OSVersionLabel = tkinter.Label(LeftFrame, text=f"Version: {mySystem.version}", font=("Acumin Variable Concept", 9),
                               bg="#ffffff")
OSVersionLabel.place(x=15, y=255)

MachineLabel = tkinter.Label(LeftFrame, text=f"Machine: {mySystem.machine}", font=("Acumin Variable Concept", 9),
                             bg="#ffffff")
MachineLabel.place(x=15, y=280)

strvar_availableRAM = tkinter.StringVar()
RAMLabel = tkinter.Label(LeftFrame, textvariable=strvar_availableRAM, font=("Acumin Variable Concept", 9), bg="#ffffff")
RAMLabel.place(x=15, y=305)
update_available_ram()

CPULabel = tkinter.Label(LeftFrame, text=f"Processor: {mySystem.processor[0:37]}", font=("Acumin Variable Concept", 9),
                         bg="#ffffff")
CPULabel.place(x=15, y=330)

# -------------------------TOP RIGHT FRAME-----------------------------------
TopRightFrame = tkinter.Frame(Body, width=470, height=230, bg="#ffffff", highlightthickness=2,
                              highlightbackground="#333333")
TopRightFrame.place(x=330, y=10)

SystemLabel = tkinter.Label(TopRightFrame, text="System", font=("Acumin Variable Concept", 10, "bold"), bg="#ffffff")
SystemLabel.place(x=10, y=10)


######################## Battery ###########################
# Function to convert seconds to hh:mm:ss
def convertTime(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%d:%02d:%02d" % (hours, minutes, seconds)

def update_battery_status():
    global batteryImg

    battery = psutil.sensors_battery() # Get the device's battery status information

    remaining_percent = battery.percent # Get remaining battery percentage
    remaining_time = convertTime(battery.secsleft)
    isPlugged = battery.power_plugged

    batteryPercentLabel.config(text=f"{remaining_percent}%")
    plugLabel.config(text=f"Plug in: {str(isPlugged)}")
    remainingTimeLabel.config(text=f"{remaining_time} remaining")

    if isPlugged == True:
        batteryImg = tkinter.PhotoImage(file="./image/laptop/charging.png")
    else:
        batteryImg = tkinter.PhotoImage(file="./image/laptop/battery.png")

    photo_batteryLabel.config(image=batteryImg)

    batteryPercentLabel.after(1000, update_battery_status)

batteryPercentLabel = tkinter.Label(TopRightFrame, font=("Acumin Variable Concept", 30, "bold"), bg="#ffffff")
batteryPercentLabel.place(x=220, y=50)

plugLabel = tkinter.Label(TopRightFrame, font=("Acumin Variable Concept", 10, "bold"), bg="#ffffff")
plugLabel.place(x=20, y=100)

remainingTimeLabel = tkinter.Label(TopRightFrame, font=("Acumin Variable Concept", 10, "bold"), bg="#ffffff")
remainingTimeLabel.place(x=200, y=100)

photo_batteryLabel = tkinter.Label(TopRightFrame, bg="#ffffff")
photo_batteryLabel.place(x=17, y=45)
update_battery_status()

##################### Speaker #########################
# Functions:
def get_current_volume_value():
    return "{: .2f}".format(volumeScale.get())

def volume_changed(event):
    device_speaker = AudioUtilities.GetSpeakers() # Get the device's speaker
    interface = device_speaker.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volumeScale = cast(interface, POINTER(IAudioEndpointVolume))
    volumeScale.SetMasterVolumeLevel(-float(get_current_volume_value()), None)

speakerLabel = tkinter.Label(TopRightFrame,text="Speaker: ", font=("Arial", 10, "bold"), bg="#ffffff")
speakerLabel.place(x=10, y=150)

# Change background of the volume scale
style = ttk.Style()
style.configure("TScale", background="#ffffff")

volumeScale = ttk.Scale(TopRightFrame, from_=60, to=0, orient="horizontal", command=volume_changed)
volumeScale.place(x=90, y=150)
volumeScale.set(10)

##################### Brightness #########################
brightnessLabel = tkinter.Label(TopRightFrame, text="Brightness: ", font=("Arial", 10, "bold"), bg="#ffffff")
brightnessLabel.place(x=10, y=180)

def get_current_brightness_value():
    return "{: .2f}".format(brightnessScale.get())

def brightness_change(event):
    screen_brightness_control.set_brightness(get_current_brightness_value())


brightnessScale = ttk.Scale(TopRightFrame, from_=0, to=100, orient="horizontal", command=brightness_change)
brightnessScale.place(x=90, y=180)

# -------------------------BOT RIGHT FRAME-----------------------------------
BotRightFrame = tkinter.Frame(Body, width=470, height=190, bg="#ffffff", highlightthickness=2,
                              highlightbackground="#333333")
BotRightFrame.place(x=330, y=255)

# Apps image and labels
appsLabel = tkinter.Label(BotRightFrame, text="Apps", bg="#ffffff", font=("Arial", 11, "bold"))
appsLabel.place(x=10, y=10)

def run_weather_app():
    subprocess.Popen(["python", "./weather_app.py"])

app1_Image = tkinter.PhotoImage(file="./image/apps/App1.png")
app1 = tkinter.Button(BotRightFrame, image=app1_Image, bg="#ffffff", bd=0, command=run_weather_app)
app1.place(x=25, y=50)

def run_to_do_list():
    subprocess.Popen(["python", "./to_do_list.py"])

app2_Image = tkinter.PhotoImage(file="./image/apps/to_do_list_app.png")
app2 = tkinter.Button(BotRightFrame, image=app2_Image, bg="#ffffff", bd=0, command=run_to_do_list)
app2.place(x=110, y=50)

def run_calendar():
    subprocess.Popen(["python", "./calendar_app.py"])

app3_Image = tkinter.PhotoImage(file="./image/apps/calendar_app.png")
app3 = tkinter.Button(BotRightFrame, image=app3_Image, bg="#ffffff", bd=0, command=run_calendar)
app3.place(x=195, y=50)

def run_shutdown_app():
    subprocess.Popen(["python", "./shutdown_app.py"])

app4_Image = tkinter.PhotoImage(file="./image/apps/shutdown_app.png")
app4 = tkinter.Button(BotRightFrame, image=app4_Image, bg="#ffffff", bd=0, command=run_shutdown_app)
app4.place(x=280, y=50)

def run_tic_tac_toe():
    subprocess.Popen(["python", "./tic_tac_toe.py"])

app5_Image = tkinter.PhotoImage(file="./image/apps/tictactoe_app.png")
app5 = tkinter.Button(BotRightFrame, image=app5_Image, bg="#ffffff", bd=0, command=run_tic_tac_toe)
app5.place(x=365, y=50)

def open_calculator():
    subprocess.Popen('calc.exe')

app6_Image = tkinter.PhotoImage(file="./image/apps/calculator_app.png")
app6 = tkinter.Button(BotRightFrame, image=app6_Image, bg="#ffffff", bd=0, command=open_calculator)
app6.place(x=25, y=117)

def open_file_manager():
    subprocess.Popen(r'explorer /select')

app7_Image = tkinter.PhotoImage(file="./image/apps/folder_app.png")
app7 = tkinter.Button(BotRightFrame, image=app7_Image, bg="#ffffff", bd=0, command=open_file_manager)
app7.place(x=110, y=120)

def open_chorme():
    wb.register("chrome", None)
    wb.open("https://www.google.com/")

app8_Image = tkinter.PhotoImage(file="./image/apps/App8.png")
app8 = tkinter.Button(BotRightFrame, image=app8_Image, bg="#ffffff", bd=0, command=open_chorme)
app8.place(x=195, y=120)

def run_white_board():
    subprocess.Popen(["python", "./white_board.py"])

app9_Image = tkinter.PhotoImage(file="./image/apps/whiteboard_app.png")
app9 = tkinter.Button(BotRightFrame, image=app9_Image, bg="#ffffff", bd=0, command=run_white_board)
app9.place(x=280, y=120)

def run_color_detect():
    subprocess.Popen(["python", "./color_detect.py"])

app10_Image = tkinter.PhotoImage(file="./image/apps/color-wheel_app.png")
app10 = tkinter.Button(BotRightFrame, image=app10_Image, bg="#ffffff", bd=0, command=run_color_detect)
app10.place(x=365, y=120)
window.mainloop()