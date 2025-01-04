from tkinter import *
import os

root = Tk()
root.title("Shutdown App")
root.geometry("400x550")
root.resizable(False, False)

# Restart button
def restart():
    os.system("shutdown /r /t 1")
restart_img = PhotoImage(file="./image/shutdown_app/restart.png")
restart_button = Button(root, borderwidth=0, cursor="hand2", command=restart, image=restart_img)
restart_button.pack()

# Shutdown button
def shutdown():
    os.system("shutdown /s /t 1")
shutdown_img = PhotoImage(file="./image/shutdown_app/shutdown.png")
shutdown_button = Button(root, borderwidth=0, cursor="hand2", command=shutdown, image=shutdown_img)
shutdown_button.pack()

# Logout button
def logout():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
Logout_img = PhotoImage(file="./image/shutdown_app/log out.png")
logout_button = Button(root, borderwidth=0, cursor="hand2", command=logout, image=Logout_img)
logout_button.pack()

root.mainloop()