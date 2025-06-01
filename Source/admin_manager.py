import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
from constants import file_path_review, admin_manager_window, font_treeview_heading, font_label, review_columns, font_button, color_bg_wh, color_bg_gr, color_bg_re

def load_reviews():
    df = pd.read_excel(file_path_review)
    df.columns = df.columns.str.strip()
    if not df.empty:
        df = df.dropna(subset=['ID', 'Name', 'Review', 'Date'])
    return df

def reject_review(review_id, refresh_reviews):
    df = load_reviews()
    df = df[df['ID'] != review_id]
    df.to_excel(file_path_review, index=False)
    messagebox.showinfo("מחיקת ביקורת", f"הביקורת {review_id} נמחקה.")
    refresh_reviews()

def open_admin_manager():
    admin_root = tk.Tk()
    admin_root.title("ניהול ביקורות")
    admin_root.geometry(admin_manager_window)
    admin_root.configure(bg="#f0f2f5")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=font_treeview_heading)
    style.configure("Treeview", font=font_label, rowheight=30)

    tree_frame = tk.Frame(admin_root, bg="#f0f2f5")
    tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    tree = ttk.Treeview(tree_frame, columns=review_columns, show='headings', selectmode="browse")
    tree.heading('ID', text='ID')
    tree.heading('Name', text='Name')
    tree.heading('Review', text='Review')
    tree.heading('Date', text='Date')

    tree.column('ID', anchor='center', width=80)
    tree.column('Name', anchor='center', width=150)
    tree.column('Review', anchor='center', width=400)
    tree.column('Date', anchor='center', width=150)

    tree.pack(fill=tk.BOTH, expand=True)

    button_frame = tk.Frame(admin_root, bg="#f0f2f5")
    button_frame.pack(pady=10)

    def refresh_reviews():
        for row in tree.get_children():
            tree.delete(row)
        df = load_reviews()
        for _, row in df.iterrows():
            tree.insert("", "end", values=(
                str(row.get('ID', '')),
                str(row.get('Name', '')),
                str(row.get('Review', '')),
                str(row.get('Date', ''))
            ))

    def reject_selected():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("לא נבחרה ביקורת", "בחר ביקורת כדי למחוק.")
            return
        confirm = messagebox.askyesno("מחיקת ביקורת", "האם אתה בטוח שברצונך למחוק את הביקורת?")
        if confirm:
            values = tree.item(selected, 'values')
            review_id = values[0]
            reject_review(review_id, refresh_reviews)

    def open_add_student_window():
        subprocess.Popen([sys.executable, "admin_add_student.py"])

    reject_button = tk.Button(button_frame, text="מחק ביקורת", command=reject_selected, bg=color_bg_re, fg=color_bg_wh, font=font_button, width=20)
    reject_button.pack(pady=10)

    add_student_button = tk.Button(button_frame, text="הוסף תלמיד חדש", command=open_add_student_window, bg=color_bg_gr,
                                   fg=color_bg_wh, font= font_button, width=20)
    add_student_button.pack(pady=10)

    refresh_reviews()
    admin_root.mainloop()
