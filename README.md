# Attendance-tracker
A simple web application to manage student attendance, built with FastAPI, MongoDB, and Jinja2 Templates.

🚀 Features
👥 Add new students (name and roll number)

✅ Mark daily attendance using checkboxes

📊 Generate monthly CSV attendance reports

🧾 User-friendly web interface

🛠 Tech Stack
⚡ FastAPI – High-performance Python web framework

☁️ MongoDB Atlas – Cloud-hosted NoSQL database

🎨 Jinja2 – Templating engine for dynamic HTML rendering

🐍 Python 3.11+

📸 Screenshots
Add Student	Mark Attendance	Generate Report

(Add screenshots in the /screenshots folder and update the filenames if different.)

📂 Folder Structure
css
Copy
Edit
project/
├── templates/
│   ├── add_student.html
│   ├── mark_attendance.html
│   ├── report_form.html
│   └── success.html
├── reports/
│   └── [Generated CSV files]
├── main.py
└── README.md
🔧 Setup Instructions
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/student-attendance-tracker.git
cd student-attendance-tracker
Create a virtual environment and activate it (optional but recommended):

bash
Copy
Edit
python -m venv venv
venv\Scripts\activate  # For Windows
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run the app:

bash
Copy
Edit
uvicorn main:app --reload
Open in browser:

cpp
Copy
Edit
http://127.0.0.1:8000
📌 To-Do / Improvements
Add login & authentication (admin/user)

Add date filter for attendance records

Improve UI styling with CSS/Bootstrap

Add export options: PDF/Excel

📃 License
MIT License

🙋‍♂️ Author
Riyaz Ahmed
Connect with me on LinkedIn
