import time
import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from datetime import datetime
from Cafeteria_menu import calorie_page
from admin_dashboard import open_admin_dashboard
import bcrypt
from constants import file_path, prefixes, lockout_duration, photo_size, font_button, font_title

df = pd.read_excel(file_path)
df.columns = df.columns.str.strip()
df['ID'] = df['ID'].astype(str)
df['Password'] = df['Password'].astype(str)
df['is_admin'] = df['is_admin'].astype(str).str.strip()


failed_attempts = {}
lockout_time = {}


def is_input_safe(value):
    return not value.startswith(prefixes)

def login():
    entered_id = entry_id.get().strip()
    password = entry_password.get().strip()


    if not is_input_safe(entered_id) or not is_input_safe(password):
        messagebox.showerror("שגיאה", "קלט לא תקין. אין להזין תווים מסוכנים בתחילת השדות.")
        return


    if entered_id in lockout_time:
        current_time = time.time()
        if (current_time - lockout_time[entered_id]) < lockout_duration:
            lock_remaining = int(lockout_duration - (current_time - lockout_time[entered_id]))
            messagebox.showerror("שגיאה", f" יותר מידי ניסיונות, תנסה שוב בעוד כ: {lock_remaining} שניות ")
            return
        else:
            del lockout_time[entered_id]

    user = df[(df['ID'] == entered_id)]
    if not user.empty:
        stored_password = user.iloc[0]["Password"]
        if bcrypt.checkpw(password.encode(), stored_password.encode()):
            failed_attempts[entered_id] = 0
            user_name = user.iloc[0]["Name"]
            status_of_payment = user.iloc[0]["Paying"]
            photo_path = user.iloc[0]["Picture"]
            is_admin = user.iloc[0]["is_admin"].lower()
            root.destroy()
            if is_admin == "yes":
                root.quit()
                open_admin_dashboard(entered_id, user_name, status_of_payment, photo_path)
            else:
                root.quit()
                show_status_page(entered_id, user_name, status_of_payment, photo_path)
        else:
            failed_attempts[entered_id] = failed_attempts.get(entered_id, 0) + 1
            if failed_attempts[entered_id] >= 3:
                lockout_time[entered_id] = time.time()
                messagebox.showerror("שגיאה", "יותר מידי ניסוינות נעשו. תנסה בעוד כ - 5 דקות")
            else:
                messagebox.showerror("שגיאה", "סיסמא או ת.ז. שגואים")
    else:
        messagebox.showerror("שגיאה", "סיסמא או ת.ז. שגואים")


def show_status_page(student_id, user_name, status_of_payment, photo_path):
    status_root = tk.Tk()
    status_root.title("משתמש")
    status_root.geometry("400x500")
    status_root.config(bg="white")
    profile_frame = tk.Frame(status_root, bg="white")
    profile_frame.pack(pady=20)

    try:
        img = Image.open(photo_path)
        img = img.resize(photo_size)
        img = img.convert("RGB")
        photo_of_student = ImageTk.PhotoImage(img)
        photo_label = tk.Label(profile_frame, image=photo_of_student, bg="white", bd=0, relief="flat")
        photo_label.config(width=100, height=100)
        photo_label.image = photo_of_student
        photo_label.pack()
    except Exception:
        photo_def = Image.new("RGB", photo_size, "gray")
        default_photo = ImageTk.PhotoImage(photo_def)
        default_label = tk.Label(profile_frame, image=default_photo, bg="white")
        default_label.image = default_photo
        default_label.pack()

    greeting_label = tk.Label(status_root, text=f"ברוכה הבאה, {user_name} ", font=("Arial", 16), bg="white")
    greeting_label.pack(pady=10)

    payment_status = "התשלום שלך התקבל" if status_of_payment == "Yes" else "התשלום שלך ממתין. אנא ודא שהושלם התשלום כדי לקבל גישה."
    status_label = tk.Label(status_root, text=payment_status, font=("Arial", 12), bg="white", wraplength=350)
    status_label.pack(pady=20)

    current_datetime = datetime.now().strftime("%B %d, %Y - %H:%M:%S")
    date_label = tk.Label(status_root, text=f"זמן כניסה: {current_datetime}", font=("Arial", 10), bg="white")
    date_label.pack(pady=10)

    menu_button = tk.Button(
        status_root,
        text="תפריט",
        command=lambda: go_to_calorie_page(status_root, student_id, user_name),
        bg="#333",
        fg="white",
        font=font_button
    )
    menu_button.pack(side="bottom", fill="x", padx=20, pady=10)

    status_root.mainloop()

def go_to_calorie_page(status_root, student_id, user_name):
    status_root.destroy()
    calorie_page(student_id, user_name)


root = tk.Tk()
root.title("כניסה לתלמיד")
root.geometry("400x300")
root.config(bg="#f5f5f5")


title_label = tk.Label(root, text="כניסה מאובטחת", font=font_title, bg="#f5f5f5", fg="#2c3e50")
title_label.pack(pady=20)

login_frame = tk.Frame(root, bg="white", bd=2, relief="groove")
login_frame.pack(pady=10, padx=20)

entry_id = ttk.Entry(login_frame, font=("Arial", 12), width=25, justify="right")
entry_id.grid(row=0, column=0, padx=10, pady=10)
label_id = tk.Label(login_frame, text=":תעודת זהות", bg="white", font=("Arial", 12), fg="#333")
label_id.grid(row=0, column=1, padx=10, pady=10, sticky="w")

entry_password = ttk.Entry(login_frame, show="*", font=("Arial", 12), width=25, justify="right")
entry_password.grid(row=1, column=0, padx=10, pady=10)
label_password = tk.Label(login_frame, text=":סיסמא", bg="white", font=("Arial", 12), fg="#333")
label_password.grid(row=1, column=1, padx=10, pady=10, sticky="w")

login_button = tk.Button(root, text="כניסה", command=login, bg="#28a745", fg="white", font=("Arial", 12, "bold"), relief="flat", width=20)
login_button.pack(pady=20)

root.mainloop()
