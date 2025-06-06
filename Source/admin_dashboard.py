import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
from Cafeteria_menu import calorie_page
from admin_manager import open_admin_manager
from constants import window_size_admin, font_title, font_button, font_treeview, color_bg_wh, font_label


def open_admin_dashboard(student_id, user_name, status_of_payment, photo_path):
    admin_root = tk.Tk()
    admin_root.title("לוח בקרת מנהל")
    admin_root.geometry(window_size_admin)
    admin_root.config(bg="white")

    profile_frame = tk.Frame(admin_root, bg=color_bg_wh)
    profile_frame.pack(pady=20)

    try:
        img = Image.open(photo_path)
        img = img.resize((100, 100))
        img = img.convert("RGB")
        photo = ImageTk.PhotoImage(img)
        photo_label = tk.Label(profile_frame, image=photo, bg="white", bd=0, relief="flat")
        photo_label.config(width=100, height=100)
        photo_label.pack()
        photo_label.image = photo


    except Exception:
        default_photo = Image.new("RGB", (100, 100), "gray")
        default_photo = ImageTk.PhotoImage(default_photo)
        default_label = tk.Label(profile_frame, image=default_photo, bg="white")
        default_label.pack()
        default_label.image = default_photo

    greeting_label = tk.Label(admin_root, text=f"ברוכה הבאה,  {user_name}", font=font_title, bg="white")
    greeting_label.pack(pady=10)

    payment_status = "התשלום שלך אושר" if status_of_payment == "Yes" else "התשלום שלך ממתין. אנא ודא שהושלם התשלום כדי לקבל גישה."
    status_label = tk.Label(admin_root, text=payment_status, font= font_label, bg="white", wraplength=350)
    status_label.pack(pady=20)

    current_datetime = datetime.now().strftime("%B %d, %Y - %H:%M:%S")
    date_label = tk.Label(admin_root, text=f"זמן כניסה: {current_datetime}", font=font_treeview, bg="white")
    date_label.pack(pady=10)

    menu_button = tk.Button(
        admin_root,
        text="תפריט",
        command= lambda: calorie_page(student_id, user_name),
        bg="#333",
        fg="white",
        font=font_button
    )
    menu_button.pack(pady=10, fill="x", padx=30)

    manage_reviews_button = tk.Button(
        admin_root,
        text="ניהול בקרה",
        command=open_admin_manager,
        bg="#007bff",
        fg="white",
        font=font_button
    )
    manage_reviews_button.pack(pady=10, fill="x", padx=30)

    admin_root.mainloop()
