import tkinter as tk
from tkinter import ttk, messagebox
import requests
import time
import re
import os
import xlwings as xw
from datetime import datetime
from googletrans import Translator

APP_ID = os.getenv('NUTRITIONIX_APP_ID', '227363a4')
API_KEY = os.getenv('NUTRITIONIX_API_KEY', '48e8b571c94d62e5dcf0658fea530bc2')
BASE_URL = 'https://trackapi.nutritionix.com/v2/natural/nutrients'

translator = Translator()
file_path_students = "Paying_students_Project1.xlsx"
file_path_review = r"C:\Users\henry\OneDrive\מסמכים\review_manager.xlsx"
user_last_request_time = {}


def translate_to_english(text):

    try:
        translated = translator.translate(text, src='iw', dest='en')
        return translated.text

    except Exception:
        return text


def translate_to_hebrew(text):

    try:
        translated = translator.translate(text, src='en', dest='iw')
        return translated.text

    except Exception:
        return text


def check_rate_limit(user_id):

    current_time = time.time()
    if user_id in user_last_request_time:
        last_request_time = user_last_request_time[user_id]

        if current_time - last_request_time < 5:
            messagebox.showwarning("יותר מידי בקשות", "לחכות כמה שניות לפני ניסיון נוסף.")
            return False

    user_last_request_time[user_id] = current_time
    return True


def validate_food_query(query):
    return bool(re.match("^[A-Za-z0-9א-ת ]{1,50}$", query))


def get_food_info(query):

    if not validate_food_query(query):
        messagebox.showerror("קלט שגוי", "בבקשה תשים שם של מאכל קיים במערכת")
        return None

    headers = {
        'x-app-id': APP_ID,
        'x-app-key': API_KEY,
        'Content-Type': 'application/json'
    }
    data = {"query": query}

    try:
        response = requests.post(BASE_URL, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException:
        messagebox.showerror("שגיאה", "ישנה בעיה במערכת, יש לנסות מאוחר יותר")
        return None

def calorie_page(student_id, student_name):
    calorie_root = tk.Tk()
    calorie_root.title("עמוד חישוב הקלוריות")
    calorie_root.geometry("600x500")
    calorie_root.config(bg="#f4f4f9")

    tk.Label(calorie_root, text="חישוב קלוריות", font=("Arial", 18, "bold"), bg="#f4f4f9", fg="#333").pack(pady=20)
    tk.Label(calorie_root, text="המידע על התזונה מבוסס על כמות אוכל ממוצעת עבור ארוחה", font=("Arial", 12), bg="#f4f4f9", fg="#555").pack(pady=10)

    def show_calories():
        food_query = entry_food.get().strip()
        if not check_rate_limit(student_id):
            return None

        food_query_english = translate_to_english(food_query)
        food_data = get_food_info(food_query_english)

        if food_data:
            try:
                food_info = food_data['foods'][0]
                translated_food_name = translate_to_hebrew(food_info['food_name'])
                result = f"{translated_food_name}\nקלוריות: {food_info['nf_calories']} קלוריות\nחלבון: {food_info['nf_protein']} גרם\nפחמימה: {food_info['nf_total_carbohydrate']} גרם\nשומנים: {food_info['nf_total_fat']} גרם"
                result_label.config(text=result)

            except KeyError:
                result_label.config(text="בעיה עם קבלת המידע, לנסות שוב מאוחר יותר")

        else:
            result_label.config(text="בעיה עם קבלת המידע, לנסות שוב מאוחר יותר")


    tk.Label(calorie_root, text="שם האוכל:", font=("Arial", 14), bg="#f4f4f9", fg="#555").pack(pady=10)
    entry_food = ttk.Entry(calorie_root, font=("Arial", 14), width=30, justify='center')
    entry_food.pack(pady=10)
    tk.Button(calorie_root, text="לחשב", command=show_calories, bg="#28a745", fg="white", font=("Arial", 12), relief="flat", width=20).pack(pady=20)
    result_label = tk.Label(calorie_root, text="", font=("Arial", 14), bg="#f4f4f9", fg="#333")
    result_label.pack(pady=10)




    def show_review_section():

        review_window = tk.Toplevel(calorie_root)
        review_window.title("לכתוב את הביקורת")
        review_window.geometry("400x300")
        review_window.config(bg="#f4f4f9")

        tk.Label(review_window, text="תרשום את הביקורת שלך עבור האוכל:", font=("Arial", 12), bg="#f4f4f9", fg="#555").pack(pady=10)
        review_text = tk.Text(review_window, height=6, width=30, font=("Arial", 12), bg="#f4f4f9", fg="#333", wrap="word")
        review_text.pack(pady=10)


        def save_review():
            review_content = review_text.get("1.0", tk.END).strip()
            if not review_content:
                messagebox.showwarning("אין ביקורת", "תרשום/תרשמי בבקשה משהו בביקורת לפני ההגשה")
                return None
            try:
                app = xw.App(visible=False)
                wb = app.books.open(file_path_review)
                ws = wb.sheets[0]
                last_row = 2
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ws.range(f"A{last_row}").value = [student_id, student_name, review_content, date, "Pending"]
                while ws.range(f"A{last_row}").value is not None:
                    last_row += 1
                wb.save()
                wb.close()
                app.quit()

                messagebox.showinfo("הביקורת נשלחה", "הביקורת שלך נשמרה")
                review_window.destroy()

            except Exception as e:
                messagebox.showerror("שגיאה", f"בעיה לשמור את הביקורת:\n{str(e)}")

        tk.Button(review_window, text="לשלוח את הביקורת", command=save_review, bg="#28a745", fg="white", font=("Arial", 12), relief="flat").pack(pady=10)

    tk.Button(calorie_root, text="לכתוב את הביקורת", command=show_review_section, bg="#007bff", fg="white", font=("Arial", 12), relief="flat", width=20).pack(pady=20)

    calorie_root.mainloop()
