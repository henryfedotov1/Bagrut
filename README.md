# Project: Cafeteria Access System

## Developer: Henry Fedotov

### Introduction

This project was developed as a final project to manage cafeteria access, student payments, and food-related feedback within a local school environment. It integrates user authentication, secure password hashing, role-based dashboards, and interaction with a food nutrition API. The system is designed with simplicity, educational structure, and core security principles in mind.

## Import Project

- You can import the project by downloading it or using those commands:
```
cd <directory_you_want>
git clone https://github.com/henryfedotov1/Bagrut.git
```

## Getting Started

### Step 1: Prepare Your Excel Files

Make sure the following Excel files are placed in the same directory as the code:

```
Paying_students_Project1.xlsx — users database
review_manager.xlsx — where the reviews are managed
```

You can initialize the hashed passwords by running:
```
convert_password_hashing.py
```
This is a one-time script to hash all plaintext passwords in the Excel file using bcrypt (hashing of the passwords).

### Step 2: Launch the Login System

Start the main login GUI by running:
```
Login_page.py
```
Enter an existing user’s credentials.

Based on your role (admin/student), the appropriate dashboard will open.

### Step 3: Use Admin Functionalities (if logged in as Admin)

#### Admins can:

##### Add new students using:
```
admin_add_student.py
```
View and manage reviews:
- Accessible using the dashboard (button: "ניהול בקרה")

### Step 4: Student Functionalities

#### Students can:

View their profile, payment status, and login time.

Click “תפריט” to:

- View food calories (via Nutritionix API)

- Submit daily meal reviews (stored with ID + date)

## Security Notes

The system includes a set of measures to ensure safety of user data and authentication:

- Password Protection: All user passwords are securely hashed with bcrypt before being saved to the Excel database.

- Brute force Defense: The server tracks failed login attempts and blocks repeated login failures to prevent brute-force attacks.

- Excel Injection Prevention: Input fields are filtered to disallow potentially dangerous characters (=, +, -, @) that could result in formula injection within Excel.

- Network Communication: While the current system uses basic TCP sockets for communication between client and server, this can be extended to include TLS encryption for enhanced security in production environments.

## Libraries

This project uses several standard and third-party Python libraries:

| Library        | Purpose                                                 |
|----------------|---------------------------------------------------------|
| `pandas`       | Read/write Excel files and manage tables of users       |
| `openpyxl`     | Direct manipulation of Excel files                      |
| `tkinter`      | GUI framework for login, menus, and admin dashboard     |
| `PIL` (Pillow) | Load and display user photos                            |
| `bcrypt`       | Hash and verify passwords securely                      |
| `requests`     | API requests to the Nutritionix service                 |
| `googletrans`  | Translate API food data into Hebrew                     |
