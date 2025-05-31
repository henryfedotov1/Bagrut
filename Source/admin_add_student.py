import tkinter as tk
from tkinter import messagebox
from openpyxl import load_workbook
import bcrypt

def is_input_safe(value):
    return not value.startswith(('=', '+', '-', '@'))

def is_password_strong(password):
    if len(password) < 4:
        return False
    if not any(c.isdigit() for c in password):
        return False
    if not any(c.isalpha() for c in password):
        return False
    return True

def add_student():
    name = entry_name.get().strip()
    student_id = entry_id.get().strip()
    paying = entry_paying.get().strip()
    picture = entry_picture.get().strip()
    password = entry_password.get().strip()
    is_admin = entry_is_admin.get().strip()

    if not (name and student_id and password):
        messagebox.showerror("שגיאה", "נא למלא את כל השדות")
        return

    if not is_input_safe(name) or not is_input_safe(student_id) or not is_input_safe(picture):
        messagebox.showerror("שגיאה", "אסור להזין תווים מסוכנים בתחילת השדות (כגון = + - @)")
        return

    if not is_password_strong(password):
        messagebox.showerror("שגיאה", "הסיסמה חלשה מדי. עליה להכיל לפחות 4 תווים, מספר ואות.")
        return

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    try:
        wb = load_workbook("Paying_students_Project1.xlsx")
        ws = wb.active
        ws.append([name, student_id, paying, picture, hashed_password, is_admin])
        wb.save("Paying_students_Project1.xlsx")
        messagebox.showinfo("הצלחה", "התלמיד נוסף בהצלחה!")
        root.destroy()
    except Exception as e:
        messagebox.showerror("שגיאה", f"שגיאה בשמירה: {e}")

root = tk.Tk()
root.title("הוספת תלמיד חדש")

tk.Label(root, text="שם:").grid(row=0, column=0, sticky="e")
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1)

tk.Label(root, text="תעודת זהות:").grid(row=1, column=0, sticky="e")
entry_id = tk.Entry(root)
entry_id.grid(row=1, column=1)

tk.Label(root, text="שילם? (כן/לא):").grid(row=2, column=0, sticky="e")
entry_paying = tk.Entry(root)
entry_paying.grid(row=2, column=1)

tk.Label(root, text="שם קובץ תמונה:").grid(row=3, column=0, sticky="e")
entry_picture = tk.Entry(root)
entry_picture.grid(row=3, column=1)

tk.Label(root, text="סיסמה:").grid(row=4, column=0, sticky="e")
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=4, column=1)

tk.Label(root, text="מנהל? (True/False):").grid(row=5, column=0, sticky="e")
entry_is_admin = tk.Entry(root)
entry_is_admin.grid(row=5, column=1)

tk.Button(root, text="הוסף תלמיד", command=add_student).grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
