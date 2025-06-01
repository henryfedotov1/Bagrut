import os

file_path = "Paying_students_Project1.xlsx"
file_path_review = "review_manager.xlsx"

max_failed_attempts = 3
lockout_duration = 300
lockout_duration_for_server = 60
login_fail_code = 0
login_student_code = 1
login_admin_code = 2

excel_headers = ['Name', 'ID', 'Paying', 'Picture', 'Password', 'is_admin']
prefixes = ('=', '+', '-', '@')

photo_color = "gray"
photo_size = (100, 100)

BASE_URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"
APP_ID = os.getenv('NUTRITIONIX_APP_ID', '227363a4')
API_KEY = os.getenv('NUTRITIONIX_API_KEY', '48e8b571c94d62e5dcf0658fea530bc2')
API_LN = 'en'
API_RES = 'he'
API_OUT = 10
API_DELAY = 30

review_columns = ['ID', 'Name', 'Review', 'Date']
reviews_approval = ["Approved", "Rejected", "Pending"]

window_size_login = "400x300"
window_size_user = "400x500"
window_size_admin = "400x550"
admin_manager_window = "950x550"
Cafeteria_menu_window = "600x500"

font_title = ("Arial", 16, "bold")
font_label = ("Arial", 12)
font_button = ("Arial", 14)
font_treeview = ("Arial", 10)
font_treeview_heading = ("Arial", 13, "bold")

color_bg_wh = "#f5f5f5"
color_bg_full_white = "#f4f4f9"
color_bg_gr = "#28a745"
color_bg_re = "#dc3545"
color_bg_dark = "#333"

server_ip = "127.0.0.1"
server_port = 9999
login_action = "login"
login_fail_code = 0
