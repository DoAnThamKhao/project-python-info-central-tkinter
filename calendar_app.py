import tkinter as tk
from tkcalendar import Calendar

root = tk.Tk()
root.resizable(False, False)  # Khóa cửa sổ với kích thước cố định

mycal = Calendar(root, setmode="day", date_pattern='dd/mm/yyyy', selectmode="day", datefont=("Arial", 12))
mycal.pack(padx=15, pady=15)

# Đặt cửa sổ vào giữa màn hình
root.geometry("380x240")

root.title("Calendar")
root.configure(bg="lightblue")

root.mainloop()