file_path = "Paying_students_Project1.xlsx"
review_file_path = "review_manager.xlsx"

max_failed_attempts = 3
lockout_duration = 300
lockout_duration_for_server = 60
login_fail_code = 0
login_student_code = 1
login_admin_code = 2

excel_headers = ["Name", "ID", "Paying", "Picture", "Password", "is_admin"]
mandotory_headers = ["ID", "Password", "is_admin", "Paying", "Picture"]
prefixes = ('=', '+', '-', '@')

photo_color = "gray"
photo_size = (100, 100)

API_BASE = "https://trackapi.nutritionix.com/v2/natural/nutrients"
API_ID = "your_app_id"
API_KEY = "your_app_key"
API_LANGUAGE = "en"
API_RESPONSE_LANGUAGE = "he"
API_REQUEST_TIMEOUT = 10
API_REQUEST_DELAY = 30

REVIEW_COLUMNS = ["ID", "Name", "Food", "Review", "Date"]
REVIEW_APPROVAL_OPTIONS = ["Approved", "Rejected", "Pending"]

WINDOW_SIZE_LOGIN = "400x300"
WINDOW_SIZE_USER = "400x500"
WINDOW_SIZE_ADMIN = "950x550"

FONT_TITLE = ("Arial", 16, "bold")
FONT_LABEL = ("Arial", 12)
FONT_BUTTON = ("Arial", 14)
FONT_TREEVIEW = ("Arial", 12)
FONT_TREEVIEW_HEADING = ("Arial", 13, "bold")

COLOR_BACKGROUND = "#f5f5f5"
COLOR_BUTTON_GREEN = "#28a745"
COLOR_BUTTON_RED = "#dc3545"
COLOR_BUTTON_DARK = "#333"

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9999
LOGIN_ACTION = "login"
LOGIN_FAIL_CODE = 0
