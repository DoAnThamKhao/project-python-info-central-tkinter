import tkinter as tk
from tkinter import messagebox, simpledialog
from tkcalendar import Calendar

root = tk.Tk()
root.resizable(False, False)  # Khóa cửa sổ với kích thước cố định

# Dữ liệu mẫu về sự kiện
event_data = {}  # Thay đổi cấu trúc dữ liệu để mỗi ngày có một danh sách sự kiện riêng
selected_dates = set()


def date_selected(event=None):
    global selected_dates
    selected_dates.add(mycal.get_date())
    update_event_list()


def update_event_list():
    event_list.delete(0, tk.END)
    for date in event_data:
        for event in event_data[date]:
            event_list.insert(tk.END, f"{date}: {event}")


def add_event():
    global selected_dates
    event = event_entry.get()
    for date in selected_dates:
        if date in event_data:
            event_data[date].append(event)
        else:
            event_data[date] = [event]
    update_event_list()
    selected_dates.clear()


def edit_event():
    selected_event = event_list.curselection()
    if selected_event:
        index = selected_event[0]
        event_info = event_list.get(index)
        date, event = event_info.split(": ")
        new_event = simpledialog.askstring("Edit Event", f"Edit event '{event}':", parent=root)
        if new_event:
            event_data[date][index] = new_event
            update_event_list()


def delete_event():
    selected_event = event_list.curselection()
    if selected_event:
        index = selected_event[0]
        event_info = event_list.get(index)
        date, event = event_info.split(": ")
        event_data[date].remove(event)
        event_list.delete(index)


mycal = Calendar(root, setmode="day", date_pattern='dd/mm/yyyy', selectmode="day", datefont=("Arial", 12))
mycal.pack(padx=15, pady=15)

mycal.bind("<<CalendarSelected>>", date_selected)

select_date_button = tk.Button(root, text="Select Date", command=date_selected, font=("Arial", 12))
select_date_button.pack(pady=5)

event_entry_label = tk.Label(root, text="Event:", font=("Arial", 12))
event_entry_label.pack(pady=5)

event_entry = tk.Entry(root, font=("Arial", 12))
event_entry.pack(pady=5, padx=10)  # Căn chỉnh lề cho ô nhập sự kiện

add_event_button = tk.Button(root, text="Add Event", command=add_event, font=("Arial", 12))
add_event_button.pack(pady=5)

edit_event_button = tk.Button(root, text="Edit Selected Event", command=edit_event, font=("Arial", 12))
edit_event_button.pack(pady=5)

event_list = tk.Listbox(root, height=8, font=("Arial", 12))
event_list.pack(pady=5, padx=10)  # Căn chỉnh lề cho ô hiển thị danh sách sự kiện

delete_event_button = tk.Button(root, text="Delete Selected Event", command=delete_event, font=("Arial", 12))
delete_event_button.pack(pady=10)

# Lấy kích thước màn hình
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Đặt cửa sổ vào giữa màn hình
window_width = 400
window_height = 650
x_position = int((screen_width - window_width) / 2)
y_position = int((screen_height - window_height) / 4)
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

root.title("Calendar")
root.configure(bg="lightblue")

root.mainloop()